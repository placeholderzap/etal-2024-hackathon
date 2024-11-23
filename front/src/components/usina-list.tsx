import Skeleton from "react-loading-skeleton";
import "react-loading-skeleton/dist/skeleton.css";
import {
  Table,
  TableBody,
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
        {usinas.map((usina) => (
          <TableRow key={usina.id}>
            <TableCell>{usina.id}</TableCell>
            <TableCell>{usina.potencia} kWp</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};
