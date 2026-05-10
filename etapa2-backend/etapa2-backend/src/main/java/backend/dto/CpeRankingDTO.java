package backend.dto;

import lombok.Data;

@Data
public class CpeRankingDTO {
    private Long id;
    private String vendorProduct;
    private Integer cveCount;
}
