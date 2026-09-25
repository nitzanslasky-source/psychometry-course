import { notFound } from "next/navigation";
import { SimulationRunner } from "@/components/sim/SimulationRunner";
import { getSimulationSection } from "@/lib/content";

export default async function SimulationPage({
  params,
}: {
  params: Promise<{ sectionId: string }>;
}) {
  const { sectionId } = await params;
  const data = getSimulationSection(sectionId);
  if (!data) notFound();
  return <SimulationRunner data={data} />;
}
