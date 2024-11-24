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
        }}
        className="h-[600px]"
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={formattedData} margin={{ left: 10, right: 10 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <ChartTooltip content={<ChartTooltipContent />} />
            <Legend />
            <Line
              dot={false}
              strokeWidth={2}
              type="linear"
              dataKey="expected"
              stroke="var(--color-expected)"
              name="Prognostico"
            />
            <Line
              enableBackground={""}
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
