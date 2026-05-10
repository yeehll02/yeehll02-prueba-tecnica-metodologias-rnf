package backend.controller;

import backend.dto.CpeRankingDTO;
import backend.service.CpeRankingService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/cpe-ranking")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class CpeRankingController {

    private final CpeRankingService service;

    @GetMapping
    public List<CpeRankingDTO> getAll() {
        return service.getAll();
    }
}
