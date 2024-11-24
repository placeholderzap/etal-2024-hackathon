"use client";

import { CidadeList } from "@/components/cidade-list";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
} from "@/components/ui/pagination";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { debounce, isEmpty } from "lodash-es";
import { parseAsInteger, parseAsString, useQueryState } from "nuqs";
import { useCallback, useMemo } from "react";
import {
  TbChevronLeft,
  TbChevronRight,
  TbChevronsLeft,
  TbChevronsRight,
} from "react-icons/tb";
import useSWR from "swr";
import { fetcher } from "../../../lib/swr";

const PAGE_SIZE_OPTIONS = [10, 20, 50, 100];

export default function Cidades() {
  const [search, setSearch] = useQueryState("cidade", parseAsString);
  const [pageSize, setPageSize] = useQueryState(
    "resultados",
    parseAsInteger.withDefault(20)
  );
  const [currentPage, setCurrentPage] = useQueryState(
    "pagina",
    parseAsInteger.withDefault(0)
  );

  const { data, error, isLoading } = useSWR(
    `${
      process.env.NEXT_PUBLIC_API_HOST
    }/cidades?limit=${pageSize}&offset=${currentPage}${
      search && search.length > 0 ? `&search=${search}` : ""
    }`,
    fetcher,
    {
      fallbackData: { results: [], count: 0, next: "", previous: "" },
    }
  );

  const totalItems = useMemo(
    () => Math.ceil(data?.count / pageSize),
    [data, pageSize]
  );

  // eslint-disable-next-line react-hooks/exhaustive-deps
  const debouncedSearch = useCallback(
    debounce(async (value: string) => {
      const trimmedValue = value.trim();
      if (isEmpty(trimmedValue)) {
        setSearch(null);
      } else if (trimmedValue.length >= 1) {
        setSearch(trimmedValue);
      }
    }, 500),
    []
  );

  const handleNextPage = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    setCurrentPage(currentPage + 1);
  };

  const handlePreviousPage = (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    setCurrentPage(currentPage - 1);
  };

  const handleStepToPage = (page: number) => {
    setCurrentPage(page);
  };

  if (error) return <div>Erro ao carregar as cidades</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Listagem de Cidades</h1>
      <div className="flex items-center gap-4">
        <Input
          placeholder="Pesquisar cidade"
          className="w-80"
          onChange={(e) => debouncedSearch(e.target.value)}
        />

        <Pagination className="justify-between mt-2">
          <div className="flex items-center gap-4 w-fit">
            <span className="text-muted-foreground whitespace-nowrap w-[200px]">
              Página {currentPage} de {totalItems}
            </span>

            <Select onValueChange={(value) => setPageSize(parseInt(value, 10))}>
              <SelectTrigger>
                <SelectValue
                  placeholder={`Exibindo ${pageSize} itens por página`}
                />
              </SelectTrigger>
              <SelectContent>
                {PAGE_SIZE_OPTIONS.map((option) => (
                  <SelectItem value={option.toString()} key={option}>
                    {option} itens por página
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <PaginationContent>
            <PaginationItem>
              <Button
                size="icon"
                variant="ghost"
                disabled={(search && search.length > 0) || currentPage === 0}
                onClick={() => handleStepToPage(0)}
              >
                <TbChevronsLeft size={24} />
              </Button>
            </PaginationItem>

            <PaginationItem>
              <Button
                size="icon"
                variant="ghost"
                disabled={(search && search.length > 0) || !data.previous}
                onClick={handlePreviousPage}
              >
                <TbChevronLeft size={24} />
              </Button>
            </PaginationItem>

            <PaginationItem>
              <Button
                size="icon"
                variant="ghost"
                disabled={(search && search.length > 0) || !data.next}
                onClick={handleNextPage}
              >
                <TbChevronRight size={24} />
              </Button>
            </PaginationItem>

            <PaginationItem>
              <Button
                size="icon"
                variant="ghost"
                disabled={
                  (search && search.length > 0) || currentPage === totalItems
                }
                onClick={() => handleStepToPage(totalItems)}
              >
                <TbChevronsRight size={24} />
              </Button>
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
      <CidadeList cidades={data.results} isLoading={isLoading} />
    </div>
  );
}
