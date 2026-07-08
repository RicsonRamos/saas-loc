import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { z } from "zod";

import { Button } from "@/components/ui/Button";
import { extrairMensagemErro } from "@/core/api/client";
import { useAuth } from "@/core/auth/AuthContext";

const loginSchema = z.object({
  email: z.string().email("Informe um e-mail válido."),
  password: z.string().min(1, "Informe a senha."),
});

type LoginForm = z.infer<typeof loginSchema>;

export function LoginPage() {
  const { usuario, carregando, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [erro, setErro] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({ resolver: zodResolver(loginSchema) });

  if (!carregando && usuario) {
    const destino = (location.state as { from?: string } | null)?.from ?? "/frota";
    return <Navigate to={destino} replace />;
  }

  async function onSubmit(dados: LoginForm) {
    setErro(null);
    try {
      await login(dados.email, dados.password);
      navigate("/frota", { replace: true });
    } catch (error) {
      setErro(extrairMensagemErro(error));
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="w-full max-w-sm rounded-lg border border-slate-200 bg-white p-6 shadow-sm"
      >
        <h1 className="mb-6 text-lg font-semibold text-slate-900">Locadora — Entrar</h1>

        <label className="mb-1 block text-sm font-medium text-slate-700">E-mail</label>
        <input
          type="email"
          className="mb-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          {...register("email")}
        />
        {errors.email && <p className="mb-2 text-xs text-red-600">{errors.email.message}</p>}

        <label className="mb-1 mt-3 block text-sm font-medium text-slate-700">Senha</label>
        <input
          type="password"
          className="mb-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          {...register("password")}
        />
        {errors.password && (
          <p className="mb-2 text-xs text-red-600">{errors.password.message}</p>
        )}

        {erro && <p className="mb-3 text-sm text-red-600">{erro}</p>}

        <Button type="submit" disabled={isSubmitting} className="mt-3 w-full">
          {isSubmitting ? "Entrando..." : "Entrar"}
        </Button>
      </form>
    </div>
  );
}
