"use client";

import moment from "moment";
import { parseAsString, useQueryState } from "nuqs";
import useSWR from "swr";
import { fetcher } from "../../lib/swr";
import { Chart } from "./chart";
import { DatePicker } from "./date-picker";

export function UsinaDetails({ id }: { id: number }) {
  const today = new Date().toISOString().split("T")[0];
  const firstDayOfTheMonth = new Date(
    new Date().getFullYear(),
    new Date().getMonth(),
    1
  ).toISOString();

  const [groupBy] = useQueryState("agrupar", parseAsString);

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

  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (error) {
    return <p>Error: {error.message}</p>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4"></h1>
      <DatePicker
        startDate={startDate}
        setStartDate={setStartDate}
        endDate={endDate}
        setEndDate={setEndDate}
      />

      <div className="w-full flex gap-4">
        <Chart data={data.geracao} />

        <div>
          {data.geracao.map((item: Detalhes) => (
            <div key={item.data}>
              <p>
                {moment(item.data).format("DD/MM/YYYY")} {item.saude}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
