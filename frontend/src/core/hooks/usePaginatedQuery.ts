import { useQuery } from "@tanstack/react-query";

import { apiClient } from "@/core/api/client";

export interface PageMeta {
  page: number;
  limit: number;
  total: number;
}

export interface Page<T> {
  data: T[];
  meta: PageMeta;
}

export function usePaginatedQuery<T>(
  queryKey: readonly unknown[],
  url: string,
  params: Record<string, unknown> = {}
) {
  return useQuery({
    queryKey: [...queryKey, params],
    queryFn: async () => {
      const { data } = await apiClient.get<Page<T>>(url, { params });
      return data;
    },
  });
}
