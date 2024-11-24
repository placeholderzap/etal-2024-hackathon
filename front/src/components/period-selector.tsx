import { Tabs, TabsList, TabsTrigger } from "./ui/tabs";

interface PeriodSelectorProps {
  onTabChange: (value: string) => void;
  selectedTab: string;
}

export const PeriodSelector = ({
  selectedTab,
  onTabChange,
}: PeriodSelectorProps) => {
  return (
    <Tabs value={selectedTab} onValueChange={onTabChange}>
      <TabsList>
        <TabsTrigger value="dia">Dia</TabsTrigger>
        <TabsTrigger value="mes">Mês</TabsTrigger>
        <TabsTrigger value="ano">Ano</TabsTrigger>
      </TabsList>
    </Tabs>
  );
};
