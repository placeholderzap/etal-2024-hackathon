interface Detalhes {
  data: string;
  id: number;
  prognostico: number;
  quantidade: number;
  saude: "ok" | "erro_medicao" | "erro_cadastro";
}
