import api from './api';

export const relatorioService = {
  
  baixarCsvFluxoCaixa: async (ano: number, mes: number): Promise<void> => {
    const response = await api.get(`/relatorios/fluxo-caixa/csv?ano=${ano}&mes=${mes}`, {
      responseType: 'blob'
    });
    downloadBlob(response.data, `extrato_${ano}_${mes}.csv`);
  },

  baixarPdfFluxoCaixa: async (ano: number, mes: number): Promise<void> => {
    const response = await api.get(`/relatorios/fluxo-caixa/pdf?ano=${ano}&mes=${mes}`, {
      responseType: 'blob'
    });
    downloadBlob(response.data, `extrato_${ano}_${mes}.pdf`);
  }
};

/**
 * Função utilitária para forçar o download no navegador simulando um clique de âncora.
 */
function downloadBlob(blobData: Blob, filename: string) {
  const url = window.URL.createObjectURL(new Blob([blobData]));
  const link = document.createElement('link');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.parentNode?.removeChild(link);
}
