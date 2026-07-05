package com.locadora.security.service;

import com.locadora.usuario.entity.Usuario;
import com.locadora.usuario.repository.PermissionRepository;
import com.locadora.usuario.repository.UsuarioRepository;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Carrega os dados do usuário e injeta Roles + Permissões Granulares na sessão do Spring Security.
 */
@Service
public class CustomUserDetailsService implements UserDetailsService {

    private final UsuarioRepository usuarioRepository;
    private final PermissionRepository permissionRepository;

    public CustomUserDetailsService(UsuarioRepository usuarioRepository,
                                  PermissionRepository permissionRepository) {
        this.usuarioRepository = usuarioRepository;
        this.permissionRepository = permissionRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        Usuario usuario = usuarioRepository.findByEmailAndDeletedAtIsNull(email)
                .orElseThrow(() -> new UsernameNotFoundException("Usuário não encontrado: " + email));

        if (!usuario.getAtivo()) {
            throw new UsernameNotFoundException("Usuário inativo: " + email);
        }

        // 1. Roles do usuário (ex: ROLE_ADMIN)
        Set<GrantedAuthority> authorities = usuario.getRoles().stream()
                .map(role -> new SimpleGrantedAuthority("ROLE_" + role.name()))
                .collect(Collectors.toSet());

        // 2. Permissões granulares do usuário (ex: CONTRATO_EXCLUIR)
        Set<String> permissionNames = permissionRepository.findPermissionNamesByUsuarioId(usuario.getId());
        permissionNames.stream()
                .map(SimpleGrantedAuthority::new)
                .forEach(authorities::add);

        return new User(
                usuario.getEmail(),
                usuario.getSenha(),
                authorities
        );
    }
}
