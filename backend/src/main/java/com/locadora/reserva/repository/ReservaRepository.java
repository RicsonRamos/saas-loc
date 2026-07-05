package com.locadora.reserva.repository;

import com.locadora.reserva.entity.Reserva;
import com.locadora.reserva.entity.StatusReserva;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ReservaRepository extends JpaRepository<Reserva, UUID> {

    Page<Reserva> findByDeletedAtIsNull(Pageable pageable);

    Optional<Reserva> findByIdAndDeletedAtIsNull(UUID id);

    @Query("SELECT COUNT(r) > 0 FROM Reserva r WHERE r.veiculo.id = :veiculoId " +
           "AND r.status IN ('RESERVADO', 'CONFIRMADO') " +
           "AND r.deletedAt IS NULL " +
           "AND r.dataInicio < :fim AND r.dataFim > :inicio " +
           "AND (:reservaId IS NULL OR r.id <> :reservaId)")
    boolean existsConflict(
            @Param("veiculoId") UUID veiculoId,
            @Param("inicio") LocalDateTime inicio,
            @Param("fim") LocalDateTime fim,
            @Param("reservaId") UUID reservaId
    );

    List<Reserva> findByDeletedAtIsNullAndDataInicioBetween(LocalDateTime start, LocalDateTime end);
}
