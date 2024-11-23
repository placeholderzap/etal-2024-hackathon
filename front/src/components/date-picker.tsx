"use client";

import moment from "moment";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { ptBR } from "date-fns/locale";
import { Calendar1 } from "lucide-react";
import { useState } from "react";
import { DateRange } from "react-day-picker";

moment.locale("pt-br");

interface DatePickerProps extends React.ComponentProps<"div"> {
  startDate: string;
  setStartDate: (startDate: string) => void;
  endDate: string;
  setEndDate: (endDate: string) => void;
  className?: string;
}

export function DatePicker({
  className,
  startDate,
  setStartDate,
  endDate,
  setEndDate,
}: DatePickerProps) {
  const [date, setDate] = useState<DateRange | undefined>({
    from: startDate ? moment(startDate).toDate() : undefined,
    to: endDate ? moment(endDate).toDate() : undefined,
  });

  const handleSelect = (range: DateRange | undefined) => {
    setDate({
      from: range?.from ? moment(range.from).toDate() : undefined,
      to: range?.to ? moment(range.to).toDate() : undefined,
    });
    if (range?.from) {
      setStartDate(moment(range.from).utc(true).format("YYYY-MM-DD"));
    }
    if (range?.to) {
      setEndDate(moment(range.to).utc(true).format("YYYY-MM-DD"));
    }
  };

  return (
    <div className={cn("grid gap-2", className)}>
      <Popover>
        <PopoverTrigger asChild>
          <Button
            id="date"
            variant={"outline"}
            className={cn(
              "w-[300px] justify-start text-left font-normal",
              !date && "text-muted-foreground"
            )}
          >
            <Calendar1 className="mr-2 h-4 w-4" />
            {date?.from ? (
              date.to ? (
                <>
                  {moment(date.from).format("ll")} -{" "}
                  {moment(date.to).format("ll")}
                </>
              ) : (
                moment(date.from).format("ll")
              )
            ) : (
              <span>Selecione uma data</span>
            )}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            locale={ptBR}
            initialFocus
            mode="range"
            defaultMonth={date?.from}
            selected={date}
            onSelect={handleSelect}
            numberOfMonths={2}
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}
