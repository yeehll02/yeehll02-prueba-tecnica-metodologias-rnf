package backend.controller;

import backend.dto.StatsDTO;
import backend.service.StatsService;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.ClassPathResource;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/stats")
@CrossOrigin(origins = "*")
@RequiredArgsConstructor
public class StatsController {

    private final StatsService service;

    @GetMapping
    public StatsDTO getStats() {
        return service.getStats();
    }

    @GetMapping("/timeline")
    public Object getTimeline() throws Exception {
        return new ObjectMapper().readValue(
            new ClassPathResource("tendencias.json").getInputStream(), Object.class);
    }
}
