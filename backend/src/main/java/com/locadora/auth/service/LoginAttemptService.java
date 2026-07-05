package com.locadora.auth.service;

import org.springframework.stereotype.Service;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Serviço in-memory para rastrear e bloquear tentativas falhas de login.
 * Mitiga ataques de quebra de senha (Brute Force).
 */
@Service
public class LoginAttemptService {

    private static final int MAX_ATTEMPTS = 5;
    private static final long LOCK_TIME_MILLIS = 15 * 60 * 1000; // 15 minutos

    // Armazena [Email -> [Tentativas, Timestamp do último erro]]
    private final ConcurrentHashMap<String, LoginTracker> attemptsCache = new ConcurrentHashMap<>();

    public void loginSucceeded(String key) {
        attemptsCache.remove(key);
    }

    public void loginFailed(String key) {
        long currentTime = System.currentTimeMillis();
        attemptsCache.compute(key, (k, tracker) -> {
            if (tracker == null) {
                return new LoginTracker(1, currentTime);
            }
            if (currentTime - tracker.lastAttempt > LOCK_TIME_MILLIS) {
                return new LoginTracker(1, currentTime); // Reseta se passou o tempo do block
            }
            tracker.attempts++;
            tracker.lastAttempt = currentTime;
            return tracker;
        });
    }

    public boolean isBlocked(String key) {
        LoginTracker tracker = attemptsCache.get(key);
        if (tracker == null) return false;
        
        if (tracker.attempts >= MAX_ATTEMPTS) {
            if (System.currentTimeMillis() - tracker.lastAttempt > LOCK_TIME_MILLIS) {
                attemptsCache.remove(key); // Acabou o tempo de castigo
                return false;
            }
            return true;
        }
        return false;
    }

    private static class LoginTracker {
        int attempts;
        long lastAttempt;

        LoginTracker(int attempts, long lastAttempt) {
            this.attempts = attempts;
            this.lastAttempt = lastAttempt;
        }
    }
}
