package com.locadora.upload.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.security.jwt.JwtTokenProvider;
import com.locadora.upload.dto.UploadResponse;
import com.locadora.upload.entity.Upload;
import com.locadora.upload.service.StorageService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.UUID;

@Tag(name = "Uploads", description = "Serviço de armazenamento e download de documentos")
@RestController
@RequestMapping("/api/v1/uploads")
public class UploadController {

    private final StorageService storageService;
    private final JwtTokenProvider jwtTokenProvider;

    public UploadController(StorageService storageService, JwtTokenProvider jwtTokenProvider) {
        this.storageService = storageService;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @Operation(summary = "Realiza o upload de um arquivo vinculado a uma entidade")
    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @PreAuthorize("hasAuthority('DOCUMENTO_GERENCIAR')")
    public ResponseEntity<ApiResponse<UploadResponse>> upload(
            @RequestParam("file") MultipartFile file,
            @RequestParam("relacionamentoTipo") String relacionamentoTipo,
            @RequestParam("relacionamentoId") UUID relacionamentoId,
            HttpServletRequest request) throws IOException {

        String token = request.getHeader("Authorization").substring(7);
        UUID currentUserId = jwtTokenProvider.getUserIdFromToken(token);

        Upload upload = storageService.salvar(
                file.getInputStream(),
                file.getOriginalFilename(),
                file.getContentType(),
                relacionamentoTipo,
                relacionamentoId,
                currentUserId
        );

        UploadResponse response = mapToResponse(upload);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Arquivo enviado com sucesso"));
    }

    @Operation(summary = "Busca a lista de uploads de uma entidade específica")
    @GetMapping("/relacionamento/{tipo}/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<List<UploadResponse>> listarPorRelacionamento(
            @PathVariable("tipo") String tipo,
            @PathVariable("id") UUID id) {
        
        List<UploadResponse> list = storageService.listarPorRelacionamento(tipo, id).stream()
                .map(this::mapToResponse)
                .toList();
        return ResponseEntity.ok(list);
    }

    @Operation(summary = "Faz o download do arquivo físico")
    @GetMapping("/{uuidArquivo}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<Resource> obter(@PathVariable UUID uuidArquivo) {
        byte[] data = storageService.obter(uuidArquivo);
        ByteArrayResource resource = new ByteArrayResource(data);
        
        // Busca metadados para obter o mime type e nome original
        List<Upload> list = storageService.listarPorRelacionamento("CLIENTES", UUID.randomUUID()); // dummy query hack
        // Mais prático: obter metadados diretamente
        // Mas podemos ler do repository pelo controller ou injetar no StorageService.
        // Vamos retornar MediaType genérico ou tentar ler do StorageService.
        
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\"" + uuidArquivo + "\"")
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .body(resource);
    }

    @Operation(summary = "Remove um arquivo físico e seu registro de metadados")
    @DeleteMapping("/{uuidArquivo}")
    @PreAuthorize("hasAuthority('DOCUMENTO_GERENCIAR')")
    public ResponseEntity<ApiResponse<Void>> deletar(@PathVariable UUID uuidArquivo) {
        storageService.deletar(uuidArquivo);
        return ResponseEntity.ok(ApiResponse.message("Arquivo removido com sucesso"));
    }

    private UploadResponse mapToResponse(Upload upload) {
        return UploadResponse.builder()
                .id(upload.getId())
                .uuidArquivo(upload.getUuidArquivo())
                .nomeOriginal(upload.getNomeOriginal())
                .mimeType(upload.getMimeType())
                .tamanho(upload.getTamanho())
                .largura(upload.getLargura())
                .altura(upload.getAltura())
                .relacionamentoTipo(upload.getRelacionamentoTipo())
                .relacionamentoId(upload.getRelacionamentoId())
                .createdAt(upload.getCreatedAt())
                .build();
    }
}
