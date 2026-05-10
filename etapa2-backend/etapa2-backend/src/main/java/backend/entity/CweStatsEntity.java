package backend.entity;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
@Table(name = "cwe_stats")
public class CweStatsEntity {

    @Id
    private String cweId;

    private Integer cveCount;
}
