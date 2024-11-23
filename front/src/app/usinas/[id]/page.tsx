import { UsinaDetails } from "@/components/usina-details";

export default function DetalhesUsina({ params }: { params: { id: string } }) {
  return (
    <div className="container mx-auto p-4">
      <UsinaDetails id={parseInt(params.id)} />
    </div>
  );
}
