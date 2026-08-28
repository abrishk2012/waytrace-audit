$p = "C:\Users\Admin\Documents\WayTrace\dashboard\app.py"
$s = [System.IO.File]::ReadAllText($p)
$nl = if ($s.Contains("`r`n")) { "`r`n" } else { "`n" }
$ok = $true

# 1. unbuffer python subprocesses so Frame N arrives live
$a = 'def run_stage(cmd, label, total_frames, bar, status):'
if (-not $s.Contains($a)) { $ok=$false; "FAIL 1" } else {
  $s = $s.Replace($a, $a); "ok 1 - run_stage found" }

$b = '    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE,'
$bn = @(
'    if cmd and cmd[0] == sys.executable:',
'        cmd = [cmd[0], "-u"] + list(cmd[1:])   # unbuffered: Frame N arrives live',
'    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE,') -join $nl
if (-not $s.Contains($b)) { $ok=$false; "FAIL 2" } else {
  $s = $s.Replace($b, $bn); "ok 2 - unbuffered" }

# 2. stage checkpoint display
$c = 'mode = st.radio("Source", ["Recorded clip", "Upload your own"], horizontal=True)'
$cn = @(
'STAGES = ["Convert", "Undistort", "Track", "Detect", "Encode"]',
'',
'',
'def draw_stages(slot, done_upto, running=None):',
'    """done_upto = number of finished stages; running = index now in progress."""',
'    parts = []',
'    for i, name in enumerate(STAGES):',
'        if i < done_upto:',
'            parts.append(f"**:green[[done]] {name}**")',
'        elif i == running:',
'            parts.append(f"**:blue[[running]] {name}**")',
'        else:',
'            parts.append(f":gray[( ) {name}]")',
'    slot.markdown("  ---  ".join(parts))',
'',
'') -join $nl
if (-not $s.Contains($c)) { $ok=$false; "FAIL 3" } else {
  $s = $s.Replace($c, $cn + $c); "ok 3 - draw_stages added" }

# 3. wire it into the run
$d = '            bar = st.progress(0.0)' + $nl + '            status = st.empty()' + $nl
$dn = @(
'            steps = st.empty()',
'            bar = st.progress(0.0)',
'            status = st.empty()',
'            draw_stages(steps, 0, 0)',
'') -join $nl
if (-not $s.Contains($d)) { $ok=$false; "FAIL 4" } else {
  $s = $s.Replace($d, $dn); "ok 4 - steps slot" }

$e = '            bar.progress(0.0)' + $nl + '            rc, tail = run_stage('
$en = @(
'            draw_stages(steps, 1, 2)',
'            bar.progress(0.0)',
'            rc, tail = run_stage(') -join $nl
if (-not $s.Contains($e)) { $ok=$false; "FAIL 5" } else {
  $s = $s.Replace($e, $en); "ok 5 - track stage marked" }

$f = '            status.write("Re-encoding for browser playback...")'
$fn = @(
'            draw_stages(steps, 4, 4)',
'            status.write("Re-encoding for browser playback...")') -join $nl
if (-not $s.Contains($f)) { $ok=$false; "FAIL 6" } else {
  $s = $s.Replace($f, $fn); "ok 6 - encode stage marked" }

$g = '            bar.progress(1.0)' + $nl + '            status.write("Done.")'
$gn = @(
'            draw_stages(steps, 5)',
'            bar.progress(1.0)',
'            status.write("Done.")') -join $nl
if (-not $s.Contains($g)) { $ok=$false; "FAIL 7" } else {
  $s = $s.Replace($g, $gn); "ok 7 - done" }

$h = '                "Running detectors...", frames, bar, status)'
$hn = '                "Running detectors...", frames, bar, status)'
if (-not $s.Contains($h)) { $ok=$false; "FAIL 8" } else { "ok 8 - detect call found" }

$i = '            rc, tail = run_stage(' + $nl + '                [sys.executable, "src/analyse_one.py", traj, out],'
$inew = @(
'            draw_stages(steps, 3, 3)',
'            rc, tail = run_stage(',
'                [sys.executable, "src/analyse_one.py", traj, out],') -join $nl
if (-not $s.Contains($i)) { $ok=$false; "FAIL 9" } else {
  $s = $s.Replace($i, $inew); "ok 9 - detect stage marked" }

if ($ok) {
  [System.IO.File]::WriteAllText($p, $s, (New-Object System.Text.UTF8Encoding $false)); "WRITTEN"
} else { "ABORTED - nothing written" }
