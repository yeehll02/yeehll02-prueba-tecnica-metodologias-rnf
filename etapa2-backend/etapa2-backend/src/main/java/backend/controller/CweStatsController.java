package backend.controller;

import backend.dto.CweStatsDTO;
import backend.service.CweStatsService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/cwe-stats")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class CweStatsController {

    private final CweStatsService service;

    @GetMapping
    public List<CweStatsDTO> getAll() {
        return service.getAll();
    }
}
