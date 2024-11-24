"use client";

import { ArrowLeft } from "lucide-react";
import moment from "moment";
import { useRouter } from "next/navigation";
import { parseAsString, useQueryState } from "nuqs";
import useSWR from "swr";
import { fetcher } from "../../lib/swr";
import { Chart } from "./chart";
import { DatePicker } from "./date-picker";
import { PeriodSelector } from "./period-selector";
import { Status } from "./status";
import { Button } from "./ui/button";

export function UsinaDetails({ id }: { id: number }) {
  const today = new Date().toISOString().split("T")[0];
  const firstDayOfTheMonth = new Date(
    new Date().getFullYear(),
    new Date().getMonth(),
    1
  )
    .toISOString()
    .split("T")[0];

  const { push } = useRouter();

  const [groupBy, setGroupBy] = useQueryState(
    "agrupar",
    parseAsString.withDefault("dia")
  );
  const [startDate, setStartDate] = useQueryState(
    "data-inicio",
    parseAsString.withDefault(firstDayOfTheMonth)
  );
  const [endDate, setEndDate] = useQueryState(
    "data-fim",
    parseAsString.withDefault(today)
  );

  const { data, isLoading, error } = useSWR(
    `${
      process.env.NEXT_PUBLIC_API_HOST
    }/usinas/${id}?start_date=${startDate}&end_date=${endDate}${
      groupBy ? `&group_by=${groupBy}` : ""
    }`,
    fetcher
  );

  const handleTabChange = (value: string) => {
    if (value === "dia") {
      setStartDate(firstDayOfTheMonth);
      setEndDate(today);
    } else if (value === "mes") {
      setStartDate(moment().startOf("year").format("YYYY-MM-DD"));
      setEndDate(today);
    } else if (value === "ano") {
      setStartDate(moment().subtract(10, "year").format("YYYY-MM-DD"));
      setEndDate(today);
    }
    setGroupBy(value);
  };

  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (error) {
    return <p>Error: {error.message}</p>;
  }

  return (
    <div>
      <div className="flex flex-col gap-2 items-start mb-4">
        <Button variant="outline" onClick={() => push("/")}>
          <ArrowLeft size={16} />
          <span className="font-semibold"> Voltar</span>
        </Button>
        <h1 className="text-2xl font-bold">Detalhes da usina {id}</h1>
      </div>

      <section className="space-y-4">
        <div className="w-full flex items-center justify-between">
          <h2 className="whitespace-nowrap text-lg">
            Geração de energia{" "}
            {groupBy === "dia"
              ? "por dia"
              : groupBy === "mes"
              ? "por mês"
              : "por ano"}{" "}
            e detecção de anomalias
          </h2>

          <div className="w-full flex items-center justify-end gap-4">
            <PeriodSelector
              selectedTab={groupBy}
              onTabChange={handleTabChange}
            />

            <DatePicker
              startDate={startDate}
              setStartDate={setStartDate}
              endDate={endDate}
              setEndDate={setEndDate}
            />
          </div>
        </div>

        <div className="w-full flex gap-4">
          <Chart data={data.geracao} />

          <div className="h-[570px] w-full overflow-y-auto space-y-2">
            {data.geracao.map((item: Detalhes, index: number) => (
              <Status
                key={item.id || index}
                saude={item.saude}
                data={item.data}
              />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
