package backend.service;

import backend.dto.CweStatsDTO;
import backend.entity.CweStatsEntity;
import backend.repository.CweStatsRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class CweStatsService {

    private final CweStatsRepository repository;

    public List<CweStatsDTO> getAll() {
        return repository.findAll().stream()
                .sorted((a, b) -> b.getCveCount().compareTo(a.getCveCount()))
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    private CweStatsDTO toDTO(CweStatsEntity e) {
        CweStatsDTO dto = new CweStatsDTO();
        dto.setCweId(e.getCweId());
        dto.setCveCount(e.getCveCount());
        return dto;
    }
}
