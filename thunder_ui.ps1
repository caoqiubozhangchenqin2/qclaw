Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

$hwnd = [IntPtr]4589934
$root = [System.Windows.Automation.AutomationElement]::FromHandle($hwnd)

# Find all elements
$conditions = @(
    [System.Windows.Automation.Condition]::TrueCondition
)

function DumpElement($el, $indent=0) {
    $sp = " " * $indent
    try {
        $name = $el.Current.Name
        $type = $el.Current.LocalizedControlType
        $auto = $el.Current.AutomationId
        if ($name -and $name.Trim()) {
            Write-Host "$sp[$type] Name='$name' ID='$auto'"
        }
        # Look for buttons, checkboxes
        $pattern = $el.GetCurrentPattern([System.Windows.Automation.AutomationElementIdentifiers]::InvokePatternId)
        if ($pattern) { Write-Host "$sp  -> InvokePattern available" }
        $selPattern = $el.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)
        if ($selPattern) { Write-Host "$sp  -> SelectionItemPattern available" }
    } catch {}
}

# Get first level children
try {
    $children = $root.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)
    Write-Host "=== Top-level children (" $children.Count "):"
    foreach ($c in $children) {
        DumpElement $c 2
    }
} catch {
    Write-Host "Error: $_"
}

# Try to find buttons specifically
try {
    $buttonCond = @{
        [System.Windows.Automation.PropertyConditionCondition]::PropertyId = [System.Windows.Automation.AutomationElementIdentifiers]::LocalizedControlTypeProperty
        Condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElementIdentifiers]::LocalizedControlTypeProperty, "button")
    }
    $allButtonCond = New-Object System.Windows.Automation.AndCondition(@(
        (New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElementIdentifiers]::LocalizedControlTypeProperty, "button")),
        (New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElementIdentifiers]::IsOffscreenProperty, $false))
    ))
    $buttons = $root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $allButtonCond)
    Write-Host "`n=== Buttons found (" $buttons.Count "):"
    foreach ($b in $buttons) {
        $name = $b.Current.Name
        $id = $b.Current.AutomationId
        Write-Host "  Button: Name='$name' ID='$id'"
    }
} catch {
    Write-Host "Button search error: $_"
}
