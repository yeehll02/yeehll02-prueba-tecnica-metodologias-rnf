package backend.service;

import backend.dto.StatsDTO;
import backend.entity.CpeRankingEntity;
import backend.entity.CweStatsEntity;
import backend.repository.CpeRankingRepository;
import backend.repository.CweStatsRepository;
import backend.repository.VulnerabilityRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class StatsService {

    private final VulnerabilityRepository vulnRepo;
    private final CweStatsRepository cweRepo;
    private final CpeRankingRepository cpeRepo;

    public StatsDTO getStats() {
        StatsDTO dto = new StatsDTO();

        dto.setTotalCves(vulnRepo.count());
        dto.setCritical(vulnRepo.count((r, q, cb) -> cb.equal(cb.upper(r.get("cvssV31BaseSeverity")), "CRITICAL")));
        dto.setHigh(vulnRepo.count((r, q, cb) -> cb.equal(cb.upper(r.get("cvssV31BaseSeverity")), "HIGH")));
        dto.setMedium(vulnRepo.count((r, q, cb) -> cb.equal(cb.upper(r.get("cvssV31BaseSeverity")), "MEDIUM")));
        dto.setLow(vulnRepo.count((r, q, cb) -> cb.equal(cb.upper(r.get("cvssV31BaseSeverity")), "LOW")));

        dto.setCisaOnly(vulnRepo.count((r, q, cb) -> cb.and(cb.isTrue(r.get("inCisa")), cb.isFalse(r.get("inNuclei")))));
        dto.setNucleiOnly(vulnRepo.count((r, q, cb) -> cb.and(cb.isFalse(r.get("inCisa")), cb.isTrue(r.get("inNuclei")))));
        dto.setBoth(vulnRepo.count((r, q, cb) -> cb.and(cb.isTrue(r.get("inCisa")), cb.isTrue(r.get("inNuclei")))));

        List<CweStatsEntity> cwes = cweRepo.findAll(Sort.by("cveCount").descending());
        if (!cwes.isEmpty()) {
            dto.setTopCwe(cwes.get(0).getCweId());
            dto.setTopCweCount(cwes.get(0).getCveCount());
        }

        List<CpeRankingEntity> cpes = cpeRepo.findAll(Sort.by("cveCount").descending());
        if (!cpes.isEmpty()) {
            dto.setTopCpe(cpes.get(0).getVendorProduct());
            dto.setTopCpeCount(cpes.get(0).getCveCount());
        }

        List<Object[]> vendors = vulnRepo.findTopVendors(PageRequest.of(0, 1));
        if (!vendors.isEmpty()) {
            dto.setTopVendor(vendors.get(0)[0].toString());
            dto.setTopVendorCount(((Number) vendors.get(0)[1]).longValue());
        }

        List<String> dates = vulnRepo.findLatestDates(PageRequest.of(0, 1));
        if (!dates.isEmpty()) {
            dto.setLastAdded(dates.get(0));
        }

        return dto;
    }
}
