package com.locadora.common.config;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.boot.autoconfigure.web.servlet.error.ErrorViewResolver;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.ModelAndView;

import java.util.Map;

/**
 * Resolutor de erro customizado para SPA (React Router).
 * Quando ocorre erro 404 em rotas que não sejam API ou arquivos estáticos,
 * redireciona internamente para index.html com status 200 OK.
 */
@Component
public class SpaErrorViewResolver implements ErrorViewResolver {

    @Override
    public ModelAndView resolveErrorView(HttpServletRequest request, HttpStatus status, Map<String, Object> model) {
        if (status == HttpStatus.NOT_FOUND) {
            String path = request.getRequestURI();
            // Evita redirecionar requisições da API, actuator ou arquivos com extensões (ex: .png, .js)
            if (!path.startsWith("/api") && !path.startsWith("/actuator") && !path.contains(".")) {
                return new ModelAndView("forward:/index.html", HttpStatus.OK);
            }
        }
        return null;
    }
}
