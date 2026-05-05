$codes = @(
    "SNOS-131","JUR-687","JUVR-276","REBD-1026","MANX-028",
    "ABF-336","EBWH-322","START-540","IPZZ-846","MNGS-052",
    "MIDA-581","START-542","SNOS-165","ABF-338","SNOS-115",
    "MIDA-597","START-548","MIDA-573","SNOS-167","MIMK-274",
    "SNOS-150","MIDA-641","DASS-881","MIDA-574","MKMP-718"
)

$baseUrl = "https://torrentkitty.net/search/"
$ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
$outFile = "$env:USERPROFILE\Desktop\magnets_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$magnetFile = "$env:USERPROFILE\Desktop\magnet_links_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

$results = @()

foreach ($code in $codes) {
    Write-Host "Searching $code ..."
    try {
        $html = Invoke-WebRequest -Uri "$baseUrl$code" -TimeoutSec 15 -UseBasicParsing -UserAgent $ua | Select-Object -ExpandProperty Content
        
        $mMatches = [regex]::Matches($html, 'magnet:\?xt=urn:btih:([A-F0-9]+)[^"<>]*"[^>]*>(?:Open|Download)</a>')
        $nMatches = [regex]::Matches($html, 'class="name">([^<]+)</td>')
        $sMatches = [regex]::Matches($html, 'class="size">([^<]+)</td>')
        
        $entries = @()
        for ($i = 0; $i -lt $mMatches.Count; $i++) {
            $ih = $mMatches[$i].Groups[1].Value
            $name = if ($i -lt $nMatches.Count) { $nMatches[$i].Groups[1].Value } else { "?" }
            $size = if ($i -lt $sMatches.Count) { $sMatches[$i].Groups[1].Value } else { "?" }
            $lc = $name.ToLower()
            $prio = 99; $tag = "[OTHER]"
            if ($lc -match "uc|uncensored") { $prio = 1; $tag = "[UC]" }
            elseif ($lc -match "-u\b|^u-|uhd") { $prio = 2; $tag = "[U]" }
            elseif ($lc -match "chinese|ch\b|中字") { $prio = 3; $tag = "[CH]" }
            elseif ($lc -match "caribbean|c-|-c\b") { $prio = 4; $tag = "[C]" }
            elseif ($lc -match "japan|japanese") { $prio = 5; $tag = "[J]" }
            elseif ($lc -match "minifile|mini") { $prio = 90; $tag = "[MINI]" }
            $entries += [PSCustomObject]@{Code=$code;Prio=$prio;Tag=$tag;Name=$name;Size=$size;Magnet="magnet:?xt=urn:btih:$ih"}
        }
        
        $sorted = $entries | Sort-Object Prio | Select-Object -First 5
        $best = $sorted | Select-Object -First 1
        $status = if ($entries.Count -gt 0) { "OK($($entries.Count))" } else { "NONE" }
        
        $results += [PSCustomObject]@{
            Code = $code
            Status = $status
            BestTag = if ($best) { $best.Tag } else { "-" }
            BestName = if ($best) { $best.Name } else { "-" }
            BestSize = if ($best) { $best.Size } else { "-" }
            BestMagnet = if ($best) { $best.Magnet } else { "" }
        }
        
        Write-Host "  -> $status | $($best.Tag) $($best.Name) [$($best.Size)]"
        Start-Sleep -Milliseconds 800
    }
    catch {
        $results += [PSCustomObject]@{Code=$code;Status="FAIL";BestTag="-";BestName="-";BestSize="-";BestMagnet=""}
        Write-Host "  -> FAIL: $($_.Exception.Message)"
    }
}

# Summary
$ts = Get-Date -Format 'yyyy-MM-dd HH:mm'
"$ts  MAGNET SEARCH RESULTS`n" | Out-File $outFile -Encoding UTF8
foreach ($r in $results) {
    "$($r.Code) | $($r.Status) | $($r.BestTag) $($r.BestName) [$($r.BestSize)]" | Add-Content $outFile -Encoding UTF8
    if ($r.BestMagnet) { "Magnet: $($r.BestMagnet)" | Add-Content $outFile -Encoding UTF8 }
    "" | Add-Content $outFile -Encoding UTF8
}

# Magnet-only list
"$ts MAGNET LINKS`n" | Out-File $magnetFile -Encoding UTF8
foreach ($r in $results) {
    if ($r.BestMagnet) { "$($r.Code): $($r.BestMagnet)" | Add-Content $magnetFile -Encoding UTF8 }
}

Write-Host "`nDone! Summary: $outFile`nMagnets: $magnetFile"

# Launch Thunder with first magnet
$first = ($results | Where-Object { $_.BestMagnet -ne "" } | Select-Object -First 1).BestMagnet
if ($first) {
    Write-Host "Launching Thunder: $first"
    start "thunder://$first"
}
