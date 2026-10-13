import ast
import contextlib
import io
import json
import tempfile
import unittest
import wave
import sys
import types
from unittest import mock
from pathlib import Path
from speech_review import findings, evaluate, require_ready

def w(text,s,e,p=.99):return dict(w=text,s=s,e=e,p=p)
def man(*lines):return dict(lines=[dict(text=t,start=a,end=b)for t,a,b in lines])

class SpeechReviewTests(unittest.TestCase):
    def test_short_fragment_after_complete_answer(self):
        m=man(('Choice number one is our answer.',0,2),('And every other choice is a trap.',4,6))
        result=findings([w('answer.',1.6,1.9),w('by?',2.2,2.55),w('And',4.2,4.4)],m)
        self.assertTrue(any(x['kind']=='transition_fragment' and 'by' in x['text']for x in result))
        self.assertTrue(any(x['kind']=='speech_gap'for x in result))
    def test_actual_stutter(self):
        m=man(('But which one is negative?',0,5))
        result=findings([w('but',1,1.3),w('but',1.5,1.8),w('which',1.9,2.2)],m)
        self.assertTrue(any(x['kind']=='local_repeat'for x in result))
    def test_overlap_ghost_not_a_stutter(self):
        m=man(('And nothing else.',0,5))
        self.assertFalse(findings([w('and',1,1.25),w('And',1.25,1.27,.2),w('nothing',1.3,1.6)],m))
    def test_math_letters_and_number_repetitions_preserved(self):
        m=man(('Q needs Q copies of Q. Three threes.',0,5))
        self.assertFalse(findings([w('q',1,1.2),w('q',1.3,1.5),w('three',2,2.3),w('three',2.4,2.7)],m))
    def test_separate_methods_preserved(self):
        m=man(('Choice number three is out.',0,5),('Choice number three is out.',10,15))
        words=[]
        for offset in (1,11):
            words += [w(t,offset+i*.3,offset+i*.3+.25)for i,t in enumerate('choice number three is out'.split())]
        self.assertFalse(any(x['kind']=='local_repeat'for x in findings(words,m)))
    def test_scripted_emphasis_preserved(self):
        m=man(('It is very very small.',0,5))
        self.assertFalse(findings([w('very',1,1.3),w('very',1.5,1.8)],m))
    def test_possible_clip_not_silence_cap(self):
        m=man(('answer',0,3));raw=[w('answer',1,1.6)]
        real=findings([],m,report={'cut_ranges':[[1.3,2]]},raw_words=raw)
        self.assertTrue(any(x['kind']=='possible_word_clip'for x in real))
        self.assertFalse(findings([],m,report={'cut_ranges':[[1.3,1.32]]},raw_words=raw))
    def test_substantive_missing_sentence_is_reviewed_not_cut(self):
        m=man(('Check the other choices first.',0,5))
        result=findings([],m,report={'verify':{'missing_sentences':[{'line':1,'sentence':'Check the other choices first.'}]}})
        self.assertTrue(any(x['kind']=='possible_missing_sentence'for x in result))
    def test_actual_two_sided_verifier_preserves_boundary_word(self):
        import numpy as np
        source=(Path(__file__).parent/'reading_to_video.py').read_text()
        fn=next(x for x in ast.parse(source).body if isinstance(x,ast.FunctionDef)and x.name=='transcribe_chunks')
        calls=[]
        class Model:
            def __init__(self,*args,**kwargs):
                self.index=0;self.kwargs=kwargs
                self.assert_local=kwargs['local_files_only']
            def transcribe(self,samples,**kwargs):
                calls.append(len(samples)/16000)
                # Same complete word appears in overlapping windows; midpoint
                # selection assigns it exactly once, with its full duration.
                a,b=(23.5,24.5)if self.index==0 else(3.5,4.5);self.index+=1
                word=types.SimpleNamespace(start=a,end=b,word='answer',probability=.99)
                return iter([types.SimpleNamespace(words=[word])]),None
        env=dict(os=__import__('os'),np=np,SR=48000,json=json,read_wav=lambda _:np.zeros(25*48000,dtype='float32'))
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'<actual verifier>','exec'),env)
        with tempfile.TemporaryDirectory()as folder,mock.patch.dict(sys.modules,{'faster_whisper':types.SimpleNamespace(WhisperModel=Model)}),contextlib.redirect_stdout(io.StringIO()):
            result=env['transcribe_chunks']('fixture.wav',str(Path(folder)/'words.json'))
        self.assertEqual(calls,[25.0,5.0])
        self.assertEqual([(x['s'],x['e'])for x in result],[(23.5,24.5)])
    def test_review_gate_hashes_and_read_only_audio(self):
        with tempfile.TemporaryDirectory()as folder:
            p=Path(folder)
            with wave.open(str(p/'clean.wav'),'wb')as f:
                f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes(b'\0'*480)
            (p/'manifest.json').write_text(json.dumps(man(('Answer.',0,1),('Next.',3,4))))
            original=(p/'clean.wav').read_bytes()
            review=evaluate(p,[w('stray',1.2,1.6)])
            self.assertFalse(review['ready'])
            with self.assertRaises(RuntimeError):require_ready(p)
            decisions={k:review[k]for k in ('audio_sha256','manifest_sha256')}
            decisions['decisions']=[dict(id=x['id'],disposition='keep',reason='Reviewed source; deliberate explanation.',reviewer='test reviewer')for x in review['findings']]
            (p/'speech-review-decisions.json').write_text(json.dumps(decisions))
            self.assertTrue(evaluate(p,[w('stray',1.2,1.6)])['ready']);require_ready(p)
            self.assertEqual(original,(p/'clean.wav').read_bytes())
            (p/'speech-review-decisions.json').write_text(json.dumps({**decisions,'decisions':[]}))
            with self.assertRaises(RuntimeError):require_ready(p)
            (p/'speech-review-decisions.json').write_text(json.dumps(decisions))
            (p/'manifest.json').write_text(json.dumps(man(('Changed.',0,1))))
            with self.assertRaises(RuntimeError):require_ready(p)
            self.assertFalse(evaluate(p,[w('stray',1.2,1.6)])['ready'])

if __name__=='__main__':unittest.main()
