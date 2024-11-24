import { Content } from "./content";

export default function Cidade({ params }: { params: { id: string } }) {
  if (!params.id) return null;

  return <Content id={params.id} />;
}
