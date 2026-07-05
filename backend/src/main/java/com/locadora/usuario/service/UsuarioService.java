package com.locadora.usuario.service;

import com.locadora.common.dto.PagedResponse;
import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.usuario.dto.UsuarioRequest;
import com.locadora.usuario.dto.UsuarioResponse;
import com.locadora.usuario.dto.UsuarioUpdateRequest;
import com.locadora.usuario.entity.Usuario;
import com.locadora.usuario.mapper.UsuarioMapper;
import com.locadora.usuario.repository.UsuarioRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

/**
 * Serviço de Usuários — Single-Tenant.
 */
@Service
public class UsuarioService {

    private static final Logger log = LoggerFactory.getLogger(UsuarioService.class);

    private final UsuarioRepository usuarioRepository;
    private final UsuarioMapper usuarioMapper;
    private final PasswordEncoder passwordEncoder;

    public UsuarioService(UsuarioRepository usuarioRepository,
                          UsuarioMapper usuarioMapper,
                          PasswordEncoder passwordEncoder) {
        this.usuarioRepository = usuarioRepository;
        this.usuarioMapper = usuarioMapper;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional
    public UsuarioResponse criar(UsuarioRequest request) {
        if (usuarioRepository.existsByEmail(request.getEmail())) {
            throw new BusinessException("E-mail já cadastrado");
        }

        Usuario usuario = usuarioMapper.toEntity(request);
        usuario.setSenha(passwordEncoder.encode(request.getSenha()));

        usuario = usuarioRepository.save(usuario);
        log.info("Usuário criado com sucesso: {}", usuario.getEmail());

        return usuarioMapper.toResponse(usuario);
    }

    @Transactional(readOnly = true)
    public PagedResponse<UsuarioResponse> listar(Pageable pageable) {
        Page<Usuario> page = usuarioRepository.findByDeletedAtIsNull(pageable);
        List<UsuarioResponse> data = page.getContent().stream()
                .map(usuarioMapper::toResponse)
                .toList();

        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    @Transactional(readOnly = true)
    public UsuarioResponse buscarPorId(UUID id) {
        return usuarioMapper.toResponse(obterUsuarioPorId(id));
    }

    @Transactional
    public UsuarioResponse atualizar(UUID id, UsuarioUpdateRequest request) {
        Usuario usuario = obterUsuarioPorId(id);
        usuarioMapper.updateEntity(request, usuario);

        if (request.getAtivo() != null) {
            usuario.setAtivo(request.getAtivo());
        }

        usuario = usuarioRepository.save(usuario);
        log.info("Usuário atualizado: {}", usuario.getEmail());

        return usuarioMapper.toResponse(usuario);
    }

    @Transactional
    public void excluir(UUID id, UUID currentUserId) {
        Usuario usuario = obterUsuarioPorId(id);

        if (usuario.getId().equals(currentUserId)) {
            throw new BusinessException("Não é possível excluir o próprio usuário");
        }

        usuario.softDelete(currentUserId);
        usuarioRepository.save(usuario);

        log.info("Usuário excluído (soft delete): {}", usuario.getEmail());
    }

    private Usuario obterUsuarioPorId(UUID id) {
        return usuarioRepository.findByIdAndDeletedAtIsNull(id)
                .orElseThrow(() -> new ResourceNotFoundException("Usuário", "id", id));
    }
}
