import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createColumnHelper } from "@tanstack/react-table";
import type { ReactNode } from "react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/Button";
import { DataTable } from "@/components/ui/DataTable";
import { PageHeader } from "@/components/ui/PageHeader";
import { PaginationControls } from "@/components/ui/PaginationControls";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient, extrairMensagemErro } from "@/core/api/client";
import { useAuth } from "@/core/auth/AuthContext";
import { usePaginatedQuery } from "@/core/hooks/usePaginatedQuery";

import { clienteSchema, type ClienteFormInput, type ClienteFormValues } from "./schema";
import { STATUS_CLIENTE_OPCOES, StatusClienteBadge } from "./StatusClienteBadge";
import type { Cliente } from "./types";

const columnHelper = createColumnHelper<Cliente>();

const CAMPOS_VAZIOS: ClienteFormInput = {
  nome: "",
  documento: "",
  rg: "",
  rg_orgao_emissor: "",
  data_nascimento: "",
  email: "",
  telefone: "",
  celular_secundario: "",
  whatsapp: "",
  cep: "",
  logradouro: "",
  numero: "",
  complemento: "",
  bairro: "",
  cidade: "",
  estado: "",
  cnh_numero: "",
  cnh_categoria: "",
  cnh_emissao: "",
  cnh_vencimento: "",
  cnh_orgao_emissor: "",
  cnh_primeira_habilitacao: "",
  cnh_ear: false,
  limite_credito: "",
  forma_pagamento_preferida: "",
  banco: "",
  agencia: "",
  conta: "",
  pix: "",
  caucao_padrao: "",
  contato_emergencia_nome: "",
  contato_emergencia_parentesco: "",
  contato_emergencia_telefone: "",
  contato_emergencia_whatsapp: "",
  status: "",
  observacoes: "",
};

function Campo({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <div>
      <label className="mb-1 block text-sm font-medium text-slate-700">{label}</label>
      {children}
    </div>
  );
}

const inputClasse =
  "w-full rounded-md border border-slate-300 px-3 py-2 text-sm disabled:bg-slate-100";

export function ClientesPage() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [busca, setBusca] = useState("");
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [erroAcao, setErroAcao] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Cliente>(
    ["clientes"],
    "/clientes",
    { page, limit, busca: busca || undefined }
  );

  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ClienteFormInput, unknown, ClienteFormValues>({
    resolver: zodResolver(clienteSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["clientes"] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(cliente: Cliente) {
    setEditandoId(cliente.id);
    reset({
      nome: cliente.nome,
      documento: cliente.documento,
      rg: cliente.rg ?? "",
      rg_orgao_emissor: cliente.rg_orgao_emissor ?? "",
      data_nascimento: cliente.data_nascimento ?? "",
      email: cliente.email ?? "",
      telefone: cliente.telefone ?? "",
      celular_secundario: cliente.celular_secundario ?? "",
      whatsapp: cliente.whatsapp ?? "",
      cep: cliente.cep ?? "",
      logradouro: cliente.logradouro ?? "",
      numero: cliente.numero ?? "",
      complemento: cliente.complemento ?? "",
      bairro: cliente.bairro ?? "",
      cidade: cliente.cidade ?? "",
      estado: cliente.estado ?? "",
      cnh_numero: cliente.cnh_numero ?? "",
      cnh_categoria: cliente.cnh_categoria ?? "",
      cnh_emissao: cliente.cnh_emissao ?? "",
      cnh_vencimento: cliente.cnh_vencimento ?? "",
      cnh_orgao_emissor: cliente.cnh_orgao_emissor ?? "",
      cnh_primeira_habilitacao: cliente.cnh_primeira_habilitacao ?? "",
      cnh_ear: cliente.cnh_ear,
      limite_credito: cliente.limite_credito ?? "",
      forma_pagamento_preferida: cliente.forma_pagamento_preferida ?? "",
      banco: cliente.banco ?? "",
      agencia: cliente.agencia ?? "",
      conta: cliente.conta ?? "",
      pix: cliente.pix ?? "",
      caucao_padrao: cliente.caucao_padrao ?? "",
      contato_emergencia_nome: cliente.contato_emergencia_nome ?? "",
      contato_emergencia_parentesco: cliente.contato_emergencia_parentesco ?? "",
      contato_emergencia_telefone: cliente.contato_emergencia_telefone ?? "",
      contato_emergencia_whatsapp: cliente.contato_emergencia_whatsapp ?? "",
      status: cliente.status,
      observacoes: cliente.observacoes ?? "",
    });
    setErroForm(null);
    setMostrarForm(true);
  }

  function fecharForm() {
    setMostrarForm(false);
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
  }

  const criarCliente = useMutation({
    mutationFn: (valores: ClienteFormValues) => apiClient.post("/clientes", valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const atualizarCliente = useMutation({
    mutationFn: (valores: ClienteFormValues) =>
      apiClient.patch(`/clientes/${editandoId}`, valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const removerCliente = useMutation({
    mutationFn: (clienteId: string) => apiClient.delete(`/clientes/${clienteId}`),
    onSuccess: () => {
      invalidar();
      setErroAcao(null);
    },
    onError: (error) => setErroAcao(extrairMensagemErro(error)),
  });

  function excluir(cliente: Cliente) {
    if (window.confirm(`Excluir o cliente ${cliente.nome}?`)) {
      removerCliente.mutate(cliente.id);
    }
  }

  const podeEditar = hasPermission("clientes:editar");

  const columns = [
    columnHelper.accessor("nome", { header: "Nome" }),
    columnHelper.accessor("documento", { header: "Documento" }),
    columnHelper.accessor("telefone", {
      header: "Telefone",
      cell: (info) => info.getValue() ?? "—",
    }),
    columnHelper.accessor("status", {
      header: "Situação",
      cell: (info) => <StatusClienteBadge status={info.getValue()} />,
    }),
    columnHelper.display({
      id: "acoes",
      header: "Ações",
      cell: (info: { row: { original: Cliente } }) => {
        const cliente = info.row.original;
        return (
          <div className="flex gap-2">
            <Link className="text-xs text-slate-700 underline" to={`/clientes/${cliente.id}`}>
              Ficha
            </Link>
            {podeEditar && (
              <>
                <button
                  className="text-xs text-blue-700 underline"
                  onClick={() => abrirEdicao(cliente)}
                >
                  Editar
                </button>
                <button
                  className="text-xs text-red-700 underline"
                  onClick={() => excluir(cliente)}
                >
                  Excluir
                </button>
              </>
            )}
          </div>
        );
      },
    }),
  ];

  return (
    <div>
      <PageHeader
        title="Clientes"
        actions={
          podeEditar && (
            <Button onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}>
              {mostrarForm ? "Cancelar" : "Novo cliente"}
            </Button>
          )
        }
      />

      <div className="mb-4">
        <input
          className="w-full max-w-sm rounded-md border border-slate-300 px-3 py-2 text-sm"
          placeholder="Buscar por nome, CPF/CNPJ ou telefone..."
          value={busca}
          onChange={(evento) => {
            setBusca(evento.target.value);
            setPage(1);
          }}
        />
      </div>

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) =>
            editandoId ? atualizarCliente.mutate(valores) : criarCliente.mutate(valores)
          )}
          className="mb-6 flex flex-col gap-6 rounded-lg border border-slate-200 bg-white p-4"
        >
          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Dados pessoais
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="Nome completo">
                <input className={inputClasse} {...register("nome")} />
                {errors.nome && <p className="text-xs text-red-600">{errors.nome.message}</p>}
              </Campo>
              <Campo label="CPF/CNPJ">
                <input
                  className={inputClasse}
                  disabled={!!editandoId}
                  {...register("documento")}
                />
                {errors.documento && (
                  <p className="text-xs text-red-600">{errors.documento.message}</p>
                )}
              </Campo>
              <Campo label="RG">
                <input className={inputClasse} {...register("rg")} />
              </Campo>
              <Campo label="Órgão emissor">
                <input className={inputClasse} {...register("rg_orgao_emissor")} />
              </Campo>
              <Campo label="Data de nascimento">
                <input type="date" className={inputClasse} {...register("data_nascimento")} />
              </Campo>
            </div>
          </fieldset>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Contatos
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="E-mail">
                <input className={inputClasse} {...register("email")} />
                {errors.email && <p className="text-xs text-red-600">{errors.email.message}</p>}
              </Campo>
              <Campo label="Celular principal">
                <input className={inputClasse} {...register("telefone")} />
              </Campo>
              <Campo label="Celular secundário">
                <input className={inputClasse} {...register("celular_secundario")} />
              </Campo>
              <Campo label="WhatsApp">
                <input className={inputClasse} {...register("whatsapp")} />
              </Campo>
            </div>
          </fieldset>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Endereço
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="CEP">
                <input className={inputClasse} {...register("cep")} />
              </Campo>
              <Campo label="Rua">
                <input className={inputClasse} {...register("logradouro")} />
              </Campo>
              <Campo label="Número">
                <input className={inputClasse} {...register("numero")} />
              </Campo>
              <Campo label="Complemento">
                <input className={inputClasse} {...register("complemento")} />
              </Campo>
              <Campo label="Bairro">
                <input className={inputClasse} {...register("bairro")} />
              </Campo>
              <Campo label="Cidade">
                <input className={inputClasse} {...register("cidade")} />
              </Campo>
              <Campo label="Estado">
                <input className={inputClasse} maxLength={2} {...register("estado")} />
              </Campo>
            </div>
          </fieldset>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              CNH
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="Número da CNH">
                <input className={inputClasse} {...register("cnh_numero")} />
              </Campo>
              <Campo label="Categoria">
                <input className={inputClasse} maxLength={5} {...register("cnh_categoria")} />
              </Campo>
              <Campo label="Data de emissão">
                <input type="date" className={inputClasse} {...register("cnh_emissao")} />
              </Campo>
              <Campo label="Data de vencimento">
                <input type="date" className={inputClasse} {...register("cnh_vencimento")} />
              </Campo>
              <Campo label="Órgão emissor">
                <input className={inputClasse} {...register("cnh_orgao_emissor")} />
              </Campo>
              <Campo label="Primeira habilitação">
                <input
                  type="date"
                  className={inputClasse}
                  {...register("cnh_primeira_habilitacao")}
                />
              </Campo>
              <div className="flex items-end gap-2">
                <input type="checkbox" id="cnh_ear" {...register("cnh_ear")} />
                <label htmlFor="cnh_ear" className="text-sm text-slate-700">
                  Exerce atividade remunerada (EAR)
                </label>
              </div>
            </div>
          </fieldset>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Dados financeiros
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="Limite de crédito">
                <input
                  type="number"
                  step="0.01"
                  className={inputClasse}
                  {...register("limite_credito")}
                />
              </Campo>
              <Campo label="Forma de pagamento preferida">
                <input className={inputClasse} {...register("forma_pagamento_preferida")} />
              </Campo>
              <Campo label="Banco">
                <input className={inputClasse} {...register("banco")} />
              </Campo>
              <Campo label="Agência">
                <input className={inputClasse} {...register("agencia")} />
              </Campo>
              <Campo label="Conta">
                <input className={inputClasse} {...register("conta")} />
              </Campo>
              <Campo label="PIX">
                <input className={inputClasse} {...register("pix")} />
              </Campo>
              <Campo label="Caução padrão">
                <input
                  type="number"
                  step="0.01"
                  className={inputClasse}
                  {...register("caucao_padrao")}
                />
              </Campo>
            </div>
          </fieldset>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Contato de emergência
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="Nome">
                <input className={inputClasse} {...register("contato_emergencia_nome")} />
              </Campo>
              <Campo label="Grau de parentesco">
                <input
                  className={inputClasse}
                  {...register("contato_emergencia_parentesco")}
                />
              </Campo>
              <Campo label="Telefone">
                <input className={inputClasse} {...register("contato_emergencia_telefone")} />
              </Campo>
              <Campo label="WhatsApp">
                <input className={inputClasse} {...register("contato_emergencia_whatsapp")} />
              </Campo>
            </div>
          </fieldset>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Situação e observações
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              {editandoId && (
                <Campo label="Situação">
                  <select className={inputClasse} {...register("status")}>
                    {STATUS_CLIENTE_OPCOES.map((opcao) => (
                      <option key={opcao.valor} value={opcao.valor}>
                        {opcao.rotulo}
                      </option>
                    ))}
                  </select>
                </Campo>
              )}
              <div className="sm:col-span-3">
                <Campo label="Observações">
                  <textarea
                    className={inputClasse}
                    rows={2}
                    {...register("observacoes")}
                  />
                </Campo>
              </div>
            </div>
          </fieldset>

          {erroForm && <p className="text-sm text-red-600">{erroForm}</p>}
          <div>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar cliente" : "Salvar cliente"}
            </Button>
          </div>
        </form>
      )}

      {erroAcao && <p className="mb-3 text-sm text-red-600">{erroAcao}</p>}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os clientes." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.data.length === 0 && (
        <EmptyState mensagem="Nenhum cliente cadastrado ainda." />
      )}
      {!isLoading && !isError && data && data.data.length > 0 && (
        <>
          <DataTable columns={columns} data={data.data} />
          <PaginationControls
            page={data.meta.page}
            limit={data.meta.limit}
            total={data.meta.total}
            onPageChange={setPage}
          />
        </>
      )}
    </div>
  );
}
