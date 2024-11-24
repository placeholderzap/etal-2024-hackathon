import { cn } from "@/lib/utils";
import { cva } from "class-variance-authority";
import moment from "moment";
import { FaInfoCircle } from "react-icons/fa";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "./ui/tooltip";

interface StatusProps {
  saude: Detalhes["saude"];
  data: Detalhes["data"];
}

const statusVariants = cva(
  "w-full flex items-center gap-3 rounded border p-2",
  {
    variants: {
      status: {
        erro_medicao: "border-red-800 bg-red-50 text-red-800",
        erro_cadastro: "border-yellow-800 bg-yellow-50 text-yellow-800",
      },
    },
  }
);

export const Status = ({ saude, data }: StatusProps) => {
  if (saude.status === "ok") return null;

  const text = {
    erro_medicao: "Falha detectada",
    erro_cadastro: "Possível erro de medição",
  };

  const description = {
    erro_medicao:
      "A geração está 70% ou mais abaixo do esperado. Isso pode indicar problemas técnicos na usina, como falhas ou sujeira nos equipamentos, ou condições climáticas desfavoráveis.",
    erro_cadastro:
      "A geração está 20% ou mais acima do esperado. Verifique se os dados de cadastro estão corretos ou se há condições climáticas excepcionais favorecendo a produção",
  };

  return (
    <TooltipProvider>
      <div className={cn(statusVariants({ status: saude.status }))}>
        <div className="">
          <div className="flex items-center gap-2">
            <p className="font-semibold">{text[saude.status]}</p>
            <Tooltip delayDuration={0}>
              <TooltipTrigger>
                <FaInfoCircle size={14} />
              </TooltipTrigger>

              <TooltipContent className="w-60">
                {description[saude.status]}
              </TooltipContent>
            </Tooltip>
          </div>
          <p>Eficiência: {(saude.eficiencia * 100).toFixed(2)}%</p>
        </div>

        <span className="ml-auto self-start">
          {moment(data).format("DD/MM/YYYY")}
        </span>
      </div>
    </TooltipProvider>
  );
};
