Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

$hwnd = [IntPtr]26612168
$root = [System.Windows.Automation.AutomationElement]::FromHandle($hwnd)

function DumpAll($el, $indent=0) {
    $sp = " " * $indent
    try {
        $name = $el.Current.Name
        $type = $el.Current.LocalizedControlType
        $auto = $el.Current.AutomationId
        $rect = $el.Current.BoundingRectangle
        if ($rect.Width -gt 5) {
            Write-Host "$sp[$type] Name='$name' ID='$auto' Rect=($($rect.X),$($rect.Y)) $($rect.Width)x$($rect.Height)"
            # Check for Invoke pattern
            try {
                $p = $el.GetCurrentPattern([System.Windows.Automation.AutomationElementIdentifiers]::InvokePatternId)
                if ($p) { Write-Host "$sp  -> CAN INVOKE" }
            } catch {}
            # Check for Toggle pattern (checkbox)
            try {
                $p = $el.GetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern)
                if ($p) { 
                    $state = $p.Current.ToggleState
                    Write-Host "$sp  -> ToggleState=$state"
                }
            } catch {}
        }
        # Recurse children
        try {
            $children = $el.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)
            foreach ($c in $children) {
                DumpAll $c ($indent+2)
            }
        } catch {}
    } catch {}
}

Write-Host "=== Dialog contents ==="
DumpAll $root
