package com.locadora.dashboard.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.dashboard.dto.DashboardResponse;
import com.locadora.dashboard.service.DashboardService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/dashboard")
@Tag(name = "Dashboard", description = "Painel Executivo e KPIs Matemáticos")
public class DashboardController {

    private final DashboardService dashboardService;

    public DashboardController(DashboardService dashboardService) {
        this.dashboardService = dashboardService;
    }

    @GetMapping("/resumo-mensal")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    @Operation(summary = "Obter Dashboard", description = "Retorna todos os KPIs (Ocupação, Finanças, Rentabilidade) do mês vigente em uma única chamada.")
    public ResponseEntity<ApiResponse<DashboardResponse>> obterResumo() {
        DashboardResponse response = dashboardService.obterDashboardMensal();
        return ResponseEntity.ok(ApiResponse.of(response));
    }
}
