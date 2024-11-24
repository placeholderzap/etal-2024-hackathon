import { useRouter } from "next/navigation";
import { PiFileMagnifyingGlassDuotone } from "react-icons/pi";
import Skeleton from "react-loading-skeleton";
import "react-loading-skeleton/dist/skeleton.css";
import { Button } from "./ui/button";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";

interface UsinaListProps {
  usinas: Usina[];
  isLoading: boolean;
}

const UsinaListSkeleton = () => (
  <Table>
    <TableHeader>
      <TableRow>
        <TableHead>Identificador</TableHead>
        <TableHead>Potência</TableHead>
        <TableHead>Ações</TableHead>
      </TableRow>
    </TableHeader>

    <TableBody>
      {[...Array(15)].map((_, index) => (
        <TableRow key={index}>
          <TableCell>
            <Skeleton height={16} />
          </TableCell>
          <TableCell>
            <Skeleton height={16} />
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
);

export const UsinaList = ({ usinas, isLoading }: UsinaListProps) => {
  const { push } = useRouter();

  const handleSeeDetails = (id: number) => {
    push(`/usinas/${id}`);
  };

  if (isLoading) {
    return <UsinaListSkeleton />;
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Identificador</TableHead>
          <TableHead>Potência</TableHead>
          <TableHead>Ações</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody>
        {usinas &&
          usinas.map((usina) => (
            <TableRow key={usina.id}>
              <TableCell>{usina.id}</TableCell>
              <TableCell>{usina.potencia} kWp</TableCell>
              <TableCell>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => handleSeeDetails(usina.id)}
                >
                  <PiFileMagnifyingGlassDuotone size={24} />
                </Button>
              </TableCell>
            </TableRow>
          ))}
      </TableBody>

      {!usinas && (
        <TableCaption className="text-black font-medium">
          Nenhuma usina encontrada
        </TableCaption>
      )}
    </Table>
  );
};
