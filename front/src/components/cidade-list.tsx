"use client";

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

interface CidadeListProps {
  cidades: Cidade[];
  isLoading: boolean;
}

const CidadeListSkeleton = () => (
  <Table>
    <TableHeader>
      <TableRow>
        <TableHead>Identificador</TableHead>
        <TableHead>Nome</TableHead>
        <TableHead>UF</TableHead>
        <TableHead>Região</TableHead>
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

export const CidadeList = ({ cidades, isLoading }: CidadeListProps) => {
  const { push } = useRouter();

  const handleSeeDetails = (id: number) => {
    push(`/cidades/${id}`);
  };

  if (isLoading) {
    return <CidadeListSkeleton />;
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Identificador</TableHead>
          <TableHead>Nome</TableHead>
          <TableHead>UF</TableHead>
          <TableHead>Região</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody>
        {cidades &&
          cidades.map((cidade) => (
            <TableRow key={cidade.id}>
              <TableCell>{cidade.id}</TableCell>
              <TableCell>{cidade.nome}</TableCell>
              <TableCell>{cidade.uf}</TableCell>
              <TableCell>{cidade.regiao}</TableCell>
              <TableCell>
                <Button
                  variant="outline"
                  size="icon"
                  onClick={() => handleSeeDetails(cidade.id)}
                >
                  <PiFileMagnifyingGlassDuotone size={24} />
                </Button>
              </TableCell>
            </TableRow>
          ))}
      </TableBody>

      {!cidades && (
        <TableCaption className="text-black font-medium">
          Nenhuma cidade encontrada
        </TableCaption>
      )}
    </Table>
  );
};
