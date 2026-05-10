package backend.service;

import backend.dto.CpeRankingDTO;
import backend.entity.CpeRankingEntity;
import backend.repository.CpeRankingRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class CpeRankingService {

    private final CpeRankingRepository repository;

    public List<CpeRankingDTO> getAll() {
        return repository.findAll().stream()
                .sorted((a, b) -> b.getCveCount().compareTo(a.getCveCount()))
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    private CpeRankingDTO toDTO(CpeRankingEntity e) {
        CpeRankingDTO dto = new CpeRankingDTO();
        dto.setId(e.getId());
        dto.setVendorProduct(e.getVendorProduct());
        dto.setCveCount(e.getCveCount());
        return dto;
    }
}
