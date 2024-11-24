"use client";

import useSWR from "swr";
import { fetcher } from "../../../../lib/swr";

export const Content = ({ id }: { id: string }) => {
  const { data, isLoading, error } = useSWR(
    `${process.env.NEXT_PUBLIC_API_HOST}/cidades/${id}`,
    fetcher
  );

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  console.log(data);
  return (
    <div>
      <h1>Content</h1>
    </div>
  );
};
