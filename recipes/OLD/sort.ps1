# Define the directory containing the HTML files
$directory = "C:\Users\carlevaler\Documents\GitHub\Web-Dev-Proj\recipes"

# Initialize an empty hashtable to store recipes
$recipes = @{}

# Loop through all HTML files in the directory
Get-ChildItem -Path $directory -Filter *.html | ForEach-Object {
    $filePath = $_.FullName
    $htmlContent = Get-Content -Path $filePath -Raw

    # Extract the recipe name
    if ($htmlContent -match '<h1>(.*?)</h1>') {
        $recipeName = $Matches[1].Trim()
    }

    # Extract ingredients
    $ingredients = @{}
    if ($htmlContent -match '(?s)<h2>Ingredients</h2>.*?<ul>(.*?)</ul>') {
        $ingredientList = $Matches[1] -split '</li>'
        $index = 1
        foreach ($ingredient in $ingredientList) {
            if ($ingredient -like '*li>*') {
                $ingredientParts = $ingredient -split '<li>'
                $ingredients["$index"] = $ingredientParts[1].Trim()
                $index++
            }
        }
    }

    # Extract instructions
    $instructions = @{}
    if ($htmlContent -match '(?s)<h2>Instructions</h2>.*?<ol>(.*?)</ol>') {
        $instructionList = $Matches[1] -split '</li>'
        $index = 1
        foreach ($instruction in $instructionList) {
            if ($instruction -like '*li>*') {
                $instructionParts = $instruction -split '<li>'
                $instructions["$index"] = $instructionParts[1].Trim()
                $index++
            }
        }
    }

    # Extract tips
    $tips = @{}
    if ($htmlContent -match '(?s)<h2>Tips</h2>.*?<ul>(.*?)</ul>') {
        $tipList = $Matches[1] -split '</li>'
        $index = 1
        foreach ($tip in $tipList) {
            if ($tip -match '<li>(.*?)</li>') {
                $tips["$index"] = $Matches[1].Trim()
                $index++
            }
        }

        $index = 1
        foreach ($tip in $tipList) {
            if ($tip -like '*li>*') {
                $tipParts = $tip -split '<li>'
                $tips["$index"] = $tipParts[1].Trim()
                $index++
            }
        }
    }

    # Add the recipe to the hashtable
    if ($recipeName) {
        $recipes[$recipeName] = @{
            "ingredients" = $ingredients
            "instructions" = $instructions
            "tips" = $tips
        }
    }
}

# Convert the hashtable to JSON and save it to a file
$jsonOutput = $recipes | ConvertTo-Json -Depth 3
$outputFile = Join-Path $directory "recipes.json"
Set-Content -Path $outputFile -Value $jsonOutput

Write-Host "Recipes have been extracted and saved to $outputFile"