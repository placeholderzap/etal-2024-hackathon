import moment from "moment";
import { useMemo } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "./ui/chart";

interface ChartProps {
  data: Detalhes[];
}

export const Chart = ({ data }: ChartProps) => {
  const formattedData = useMemo(
    () =>
      data.map((item) => ({
        date: moment(item.data).format("DD/MM/YYYY"),
        expected: item.prognostico,
        generated: item.quantidade,
        error: item.saude !== "ok" ? item.saude : undefined,
      })),
    [data]
  );

  return (
    <>
      <ChartContainer
        config={{
          expected: {
            label: "Prognostico",
            color: "hsl(var(--chart-1))",
          },
          generated: {
            label: "Geração",
            color: "hsl(var(--chart-2))",
          },
          error: {
            label: "Saúde",
            color: "hsl(var(--chart-3))",
          },
        }}
        className="h-[800px]"
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={formattedData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis label="kWh" />
            <ChartTooltip content={<ChartTooltipContent />} />
            <Legend />
            <Line
              dot={false}
              strokeWidth={2}
              type="linear"
              dataKey="expected"
              accentHeight={0}
              stroke="var(--color-expected)"
              name="Prognostico"
            />
            <Line
              strokeWidth={1.5}
              type="linear"
              dataKey="generated"
              stroke="var(--color-generated)"
              name="Geração"
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>
    </>
  );
};
