interface Detalhes {
  data: string;
  id?: number;
  prognostico: number;
  quantidade: number;
  saude: {
    status: "ok" | "erro_medicao" | "erro_cadastro";
    eficiencia: number;
  };
}
