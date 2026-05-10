package backend.repository;

import backend.entity.CweStatsEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CweStatsRepository extends JpaRepository<CweStatsEntity, String> {
}
