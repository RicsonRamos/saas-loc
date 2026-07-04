package com.locadora.empresa.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.empresa.dto.EmpresaResponse;
import com.locadora.empresa.dto.RegistroEmpresaRequest;
import com.locadora.empresa.entity.Empresa;
import com.locadora.empresa.mapper.EmpresaMapper;
import com.locadora.empresa.repository.EmpresaRepository;
import com.locadora.usuario.entity.Role;
import com.locadora.usuario.entity.Usuario;
import com.locadora.usuario.repository.UsuarioRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Set;
import java.util.UUID;

/**
 * Serviço de Empresa.
 * Conforme 08-guard-rails.md: toda regra de negócio pertence aos Services.
 */
@Service
public class EmpresaService {

    private static final Logger log = LoggerFactory.getLogger(EmpresaService.class);

    private final EmpresaRepository empresaRepository;
    private final UsuarioRepository usuarioRepository;
    private final EmpresaMapper empresaMapper;
    private final PasswordEncoder passwordEncoder;

    public EmpresaService(EmpresaRepository empresaRepository,
                          UsuarioRepository usuarioRepository,
                          EmpresaMapper empresaMapper,
                          PasswordEncoder passwordEncoder) {
        this.empresaRepository = empresaRepository;
        this.usuarioRepository = usuarioRepository;
        this.empresaMapper = empresaMapper;
        this.passwordEncoder = passwordEncoder;
    }

    /**
     * Registra uma nova empresa (tenant) com seu primeiro usuário administrador.
     * O id da empresa torna-se o tenant_id para todos os dados desta empresa.
     */
    @Transactional
    public EmpresaResponse registrar(RegistroEmpresaRequest request) {
        // Validar CNPJ único
        if (empresaRepository.existsByCnpj(request.getCnpj())) {
            throw new BusinessException("CNPJ já cadastrado");
        }

        // Validar email único
        if (usuarioRepository.existsByEmail(request.getEmailAdmin())) {
            throw new BusinessException("E-mail já cadastrado");
        }

        // Criar empresa
        Empresa empresa = Empresa.builder()
                .nomeFantasia(request.getNomeFantasia())
                .razaoSocial(request.getRazaoSocial())
                .cnpj(request.getCnpj())
                .ativo(true)
                .build();

        // Para empresa, o tenant_id é o próprio id
        // Salvar primeiro para gerar o UUID
        empresa.setTenantId(UUID.randomUUID()); // Placeholder - será o próprio id
        empresa = empresaRepository.save(empresa);

        // Atualizar tenant_id para ser o próprio id
        empresa.setTenantId(empresa.getId());
        empresa = empresaRepository.save(empresa);

        // Criar primeiro usuário administrador
        Usuario admin = Usuario.builder()
                .nome(request.getNomeAdmin())
                .email(request.getEmailAdmin())
                .senha(passwordEncoder.encode(request.getSenhaAdmin()))
                .tenantId(empresa.getId())
                .ativo(true)
                .roles(Set.of(Role.ADMIN))
                .build();
        admin.setTenantId(empresa.getId());

        usuarioRepository.save(admin);

        log.info("Nova empresa registrada: {} (CNPJ: {})", empresa.getNomeFantasia(), empresa.getCnpj());

        return empresaMapper.toResponse(empresa);
    }

    @Transactional(readOnly = true)
    public EmpresaResponse buscarPorId(UUID id) {
        Empresa empresa = empresaRepository.findById(id)
                .filter(e -> !e.isDeleted())
                .orElseThrow(() -> new ResourceNotFoundException("Empresa", "id", id));
        return empresaMapper.toResponse(empresa);
    }
}
