import { useState } from "react";
import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "@/core/auth/AuthContext";

const links = [
  { to: "/", label: "Dashboard" },
  { to: "/frota", label: "Frota" },
  { to: "/clientes", label: "Clientes" },
  { to: "/contratos", label: "Contratos" },
  { to: "/manutencoes", label: "Manutenções" },
  { to: "/financeiro", label: "Financeiro" },
];

export function Layout() {
  const { usuario, logout } = useAuth();
  const [menuAberto, setMenuAberto] = useState(false);

  return (
    <div className="flex min-h-screen flex-col md:flex-row">
      <header className="flex items-center justify-between border-b border-slate-200 bg-white px-4 py-3 md:hidden">
        <span className="font-semibold text-slate-900">Locadora</span>
        <button
          type="button"
          aria-label={menuAberto ? "Fechar menu" : "Abrir menu"}
          onClick={() => setMenuAberto((v) => !v)}
          className="rounded-md border border-slate-300 px-3 py-1.5 text-sm text-slate-700"
        >
          {menuAberto ? "Fechar" : "Menu"}
        </button>
      </header>

      {menuAberto && (
        <div
          className="fixed inset-0 z-20 bg-slate-900/40 md:hidden"
          onClick={() => setMenuAberto(false)}
        />
      )}

      <aside
        className={`z-30 flex w-64 flex-col border-r border-slate-200 bg-white transition-transform duration-200 md:static md:w-56 md:translate-x-0 md:transition-none ${
          menuAberto ? "fixed inset-y-0 left-0 translate-x-0" : "fixed inset-y-0 left-0 -translate-x-full md:flex"
        }`}
      >
        <div className="hidden border-b border-slate-200 px-4 py-4 font-semibold md:block">
          Locadora
        </div>
        <nav className="flex flex-1 flex-col gap-1 p-2">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === "/"}
              onClick={() => setMenuAberto(false)}
              className={({ isActive }) =>
                `rounded-md px-3 py-2 text-sm ${
                  isActive ? "bg-slate-900 text-white" : "text-slate-700 hover:bg-slate-100"
                }`
              }
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-slate-200 p-3 text-sm text-slate-600">
          <p className="truncate font-medium text-slate-900">{usuario?.nome}</p>
          <p className="truncate text-xs text-slate-500">{usuario?.role}</p>
          <button onClick={logout} className="mt-2 text-xs text-slate-500 underline">
            Sair
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto p-4 sm:p-6">
        <Outlet />
      </main>
    </div>
  );
}
