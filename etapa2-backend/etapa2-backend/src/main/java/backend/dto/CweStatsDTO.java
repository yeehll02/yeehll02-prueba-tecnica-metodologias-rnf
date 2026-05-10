package backend.dto;

import lombok.Data;

@Data
public class CweStatsDTO {
    private String cweId;
    private Integer cveCount;
}
