import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "@/core/auth/AuthContext";

const links = [
  { to: "/", label: "Dashboard" },
  { to: "/frota", label: "Frota" },
  { to: "/clientes", label: "Clientes" },
  { to: "/motoristas", label: "Motoristas" },
  { to: "/contratos", label: "Contratos" },
  { to: "/manutencoes", label: "Manutenções" },
  { to: "/financeiro", label: "Financeiro" },
];

export function Layout() {
  const { usuario, logout } = useAuth();

  return (
    <div className="flex min-h-screen">
      <aside className="flex w-56 flex-col border-r border-slate-200 bg-white">
        <div className="border-b border-slate-200 px-4 py-4 font-semibold">Locadora</div>
        <nav className="flex flex-1 flex-col gap-1 p-2">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === "/"}
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
      <main className="flex-1 overflow-y-auto p-6">
        <Outlet />
      </main>
    </div>
  );
}
