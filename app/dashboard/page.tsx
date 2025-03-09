"use client"

import { useState } from "react"
import { format } from "date-fns"
import { 
  CalendarIcon, 
  Download, 
  RefreshCw, 
  AlertTriangle, 
  Flame, 
  Plus, 
  Minus, 
  Layers, 
  Info,
  Wind,
  Thermometer,
  Droplets,
  MapPin,
  AlertCircle,
  CheckCircle2
} from "lucide-react"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { cn } from "@/lib/utils"
import { ThemeToggle } from "@/components/ui/theme-toggle"
import { Badge } from "@/components/ui/badge"

// Mock data for demonstration
const countyData = [
  {
    id: "la",
    name: "Los Angeles County",
    score: 47,
    riskLevel: "Moderate",
    riskColor: "yellow",
    recentFires: 20,
    heatMW: 600,
    firmsScore: 49,
    historicalAvg: "4 fires/week",
    historicalScore: 46,
    burnSuggestion: "Consider controlled burns in yellow zones, particularly in the northern regions.",
    coordinates: "34.052, -118.243",
    suitabilityScore: 78,
    weatherConditions: {
      temperature: 72,
      humidity: 45,
      windSpeed: 8,
      windDirection: "NW"
    },
    hazardProximity: "Medium",
    firePersonnel: 12,
    equipmentStatus: "Ready",
    permitStatus: "Pending"
  },
  {
    id: "sf",
    name: "San Francisco County",
    score: 32,
    riskLevel: "Low",
    riskColor: "green",
    recentFires: 8,
    heatMW: 250,
    firmsScore: 35,
    historicalAvg: "2 fires/week",
    historicalScore: 28,
    burnSuggestion: "Low risk areas require standard monitoring. No immediate controlled burn actions recommended.",
    coordinates: "37.77, -122.427",
    suitabilityScore: 85,
    weatherConditions: {
      temperature: 68,
      humidity: 52,
      windSpeed: 5,
      windDirection: "W"
    },
    hazardProximity: "Low",
    firePersonnel: 15,
    equipmentStatus: "Ready",
    permitStatus: "Approved"
  },
]

// Controlled burn recommendations
const burnRecommendations = [
  "Assess the location for potential hazards and implement appropriate safety measures.",
  "Monitor the weather conditions closely and be prepared to abort the burn if conditions become unfavorable.",
  "Have trained personnel and appropriate equipment on-site to manage the fire and respond to any unexpected developments.",
  "Consider conducting a test burn to assess the fire behavior and adjust the burn plan as necessary.",
  "Notify local authorities and obtain any necessary permits before conducting the controlled burn."
]

// Potential limitations
const burnLimitations = [
  {
    title: "Proximity to potential hazards",
    description: "The suitability score does not account for the proximity of the location to potential hazards, such as buildings, power lines, or other flammable materials."
  },
  {
    title: "Unpredictable weather conditions",
    description: "Although the current weather conditions are favorable for a controlled burn, weather conditions can change rapidly."
  },
  {
    title: "Fire behavior",
    description: "Even with favorable conditions, fire behavior can be unpredictable. It is essential to have trained personnel and appropriate equipment on-site."
  }
]

export default function DashboardPage() {
  const [date, setDate] = useState<Date>(new Date())
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [showFirePoints, setShowFirePoints] = useState(false)
  const [showHistorical, setShowHistorical] = useState(false)
  const [selectedCounty, setSelectedCounty] = useState(countyData[1]) // Default to SF with better burn conditions

  const handleRefresh = () => {
    setIsRefreshing(true)
    // Simulate API call
    setTimeout(() => {
      setIsRefreshing(false)
    }, 1500)
  }

  const handleExport = () => {
    alert("Exporting burn assessment data...")
  }

  const handleSendWarning = () => {
    alert(`Initiating controlled burn protocol for ${selectedCounty.name} with suitability score: ${selectedCounty.suitabilityScore}`)
  }

  const getRiskColorClass = (color: string) => {
    switch (color) {
      case "green":
        return "bg-emerald-500"
      case "yellow":
        return "bg-amber-400"
      case "orange":
        return "bg-orange-500"
      case "red":
        return "bg-red-600"
      default:
        return "bg-gray-400"
    }
  }

  const getSuitabilityColor = (score: number) => {
    if (score >= 80) return "text-emerald-500"
    if (score >= 60) return "text-amber-400"
    if (score >= 40) return "text-orange-500"
    return "text-red-600"
  }

  const getHazardColor = (level: string) => {
    switch (level.toLowerCase()) {
      case "low":
        return "bg-emerald-500"
      case "medium":
        return "bg-amber-400"
      case "high":
        return "bg-red-600"
      default:
        return "bg-gray-400"
    }
  }

  const getPermitStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "approved":
        return "bg-emerald-500"
      case "pending":
        return "bg-amber-400"
      case "denied":
        return "bg-red-600"
      default:
        return "bg-gray-400"
    }
  }

  return (
    <TooltipProvider>
      <div className="flex flex-col h-screen bg-white dark:bg-gray-900">
        {/* Top Bar */}
        <header className="flex items-center justify-between p-4 border-b bg-white dark:bg-gray-800 dark:border-gray-700 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex items-center">
              <Flame className="h-7 w-7 text-red-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight dark:text-white">BurnAI Controlled Burn Assessment</h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">AI-Powered Burn Planning & Risk Analysis</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <ThemeToggle />
            
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline" className="justify-start text-left font-normal h-10 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200">
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {format(date, "MMMM d, yyyy")}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="end">
                <Calendar mode="single" selected={date} onSelect={(date) => date && setDate(date)} initialFocus />
              </PopoverContent>
            </Popover>

            <Button variant="outline" size="icon" onClick={handleRefresh} disabled={isRefreshing} className="h-10 w-10 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-200">
              <RefreshCw className={cn("h-4 w-4", isRefreshing && "animate-spin")} />
            </Button>
          </div>
        </header>

        {/* Main Content */}
        <div className="flex flex-1 overflow-hidden">
          {/* Side Panel */}
          <div className="w-[350px] border-r overflow-y-auto bg-gray-50 dark:bg-gray-800 dark:border-gray-700 p-5">
            <h2 className="text-xl font-semibold mb-4 dark:text-white">County Burn Assessment</h2>

            <div className="space-y-6">
              {countyData.map((county) => (
                <Card
                  key={county.id}
                  className={cn(
                    "border-2",
                    county.id === selectedCounty.id ? "border-blue-500" : "border-transparent",
                    "cursor-pointer hover:border-blue-300 transition-colors",
                  )}
                  onClick={() => setSelectedCounty(county)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-lg font-medium">{county.name}</h3>
                      <Badge className={cn(getPermitStatusColor(county.permitStatus))}>
                        {county.permitStatus}
                      </Badge>
                    </div>

                    <div className="mb-3">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium">Burn Suitability: {county.suitabilityScore}/100</span>
                      </div>
                      <div className="h-3 w-full bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className={cn("h-full rounded-full", county.suitabilityScore >= 80 ? "bg-emerald-500" : county.suitabilityScore >= 60 ? "bg-amber-400" : "bg-red-600")}
                          style={{ width: `${county.suitabilityScore}%` }}
                        />
                      </div>
                    </div>
                    
                    <div className="flex items-center text-xs text-gray-500 mt-2">
                      <MapPin className="h-3 w-3 mr-1" />
                      <span>{county.coordinates}</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            <Separator className="my-5" />

            <div className="space-y-5">
              <div>
                <h3 className="text-lg font-semibold mb-3 dark:text-white">Current Conditions</h3>

                <div className="space-y-4 text-sm">
                  <div className="grid grid-cols-2 gap-2">
                    <div className="bg-white dark:bg-gray-700 p-3 rounded-md border dark:border-gray-600">
                      <div className="flex items-center text-xs text-gray-500 dark:text-gray-400 mb-1">
                        <Thermometer className="h-3 w-3 mr-1" />
                        <span>Temperature</span>
                      </div>
                      <div className="text-lg font-semibold dark:text-white">{selectedCounty.weatherConditions.temperature}°F</div>
                    </div>
                    <div className="bg-white dark:bg-gray-700 p-3 rounded-md border dark:border-gray-600">
                      <div className="flex items-center text-xs text-gray-500 dark:text-gray-400 mb-1">
                        <Droplets className="h-3 w-3 mr-1" />
                        <span>Humidity</span>
                      </div>
                      <div className="text-lg font-semibold dark:text-white">{selectedCounty.weatherConditions.humidity}%</div>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div className="bg-white dark:bg-gray-700 p-3 rounded-md border dark:border-gray-600">
                      <div className="flex items-center text-xs text-gray-500 dark:text-gray-400 mb-1">
                        <Wind className="h-3 w-3 mr-1" />
                        <span>Wind Speed</span>
                      </div>
                      <div className="text-lg font-semibold dark:text-white">{selectedCounty.weatherConditions.windSpeed} mph</div>
                    </div>
                    <div className="bg-white dark:bg-gray-700 p-3 rounded-md border dark:border-gray-600">
                      <div className="flex items-center text-xs text-gray-500 dark:text-gray-400 mb-1">
                        <Wind className="h-3 w-3 mr-1" />
                        <span>Wind Direction</span>
                      </div>
                      <div className="text-lg font-semibold dark:text-white">{selectedCounty.weatherConditions.windDirection}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold mb-3 dark:text-white">Burn Readiness</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between bg-white dark:bg-gray-700 p-3 rounded-md border dark:border-gray-600">
                    <div className="flex items-center gap-2">
                      <AlertCircle className="h-4 w-4 text-amber-500" />
                      <Label className="text-sm dark:text-gray-300">
                        Hazard Proximity
                      </Label>
                    </div>
                    <Badge className={cn(getHazardColor(selectedCounty.hazardProximity))}>
                      {selectedCounty.hazardProximity}
                    </Badge>
                  </div>

                  <div className="flex items-center justify-between bg-white dark:bg-gray-700 p-3 rounded-md border dark:border-gray-600">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="h-4 w-4 text-blue-500" />
                      <Label className="text-sm dark:text-gray-300">
                        Fire Personnel
                      </Label>
                    </div>
                    <span className="text-sm font-medium">{selectedCounty.firePersonnel} Ready</span>
                  </div>

                  <div className="flex items-center justify-between bg-white dark:bg-gray-700 p-3 rounded-md border dark:border-gray-600">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-500" />
                      <Label className="text-sm dark:text-gray-300">
                        Equipment Status
                      </Label>
                    </div>
                    <span className="text-sm font-medium">{selectedCounty.equipmentStatus}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="flex-1 overflow-y-auto p-6 bg-gray-100 dark:bg-gray-900">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Map Container */}
              <div className="relative bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden h-[400px]">
                <div className="absolute inset-0 bg-[url('/placeholder.svg?height=800&width=1200')] bg-cover bg-center">
                  {/* LA County simulation */}
                  <div
                    className="absolute left-[45%] top-[65%] w-[15%] h-[15%] bg-amber-400 bg-opacity-70 border-2 border-white cursor-pointer hover:bg-opacity-90 transition-all"
                    onClick={() => setSelectedCounty(countyData[0])}
                  >
                    <Tooltip>
                      <TooltipTrigger className="w-full h-full" />
                      <TooltipContent>
                        <p className="font-medium">Los Angeles County</p>
                        <p>Suitability: 78/100</p>
                      </TooltipContent>
                    </Tooltip>
                  </div>

                  {/* SF County simulation */}
                  <div
                    className="absolute left-[20%] top-[30%] w-[8%] h-[8%] bg-emerald-500 bg-opacity-70 border-2 border-white cursor-pointer hover:bg-opacity-90 transition-all"
                    onClick={() => setSelectedCounty(countyData[1])}
                  >
                    <Tooltip>
                      <TooltipTrigger className="w-full h-full" />
                      <TooltipContent>
                        <p className="font-medium">San Francisco County</p>
                        <p>Suitability: 85/100</p>
                      </TooltipContent>
                    </Tooltip>
                  </div>

                  {/* Fire points (conditionally rendered) */}
                  {showFirePoints && (
                    <>
                      <div className="absolute left-[48%] top-[67%] text-orange-600">
                        <Flame className="h-5 w-5" />
                      </div>
                      <div className="absolute left-[50%] top-[64%] text-orange-600">
                        <Flame className="h-5 w-5" />
                      </div>
                      <div className="absolute left-[21%] top-[31%] text-orange-600">
                        <Flame className="h-5 w-5" />
                      </div>
                    </>
                  )}

                  {/* Historical hotspots (conditionally rendered) */}
                  {showHistorical && (
                    <>
                      <div className="absolute left-[46%] top-[66%] w-3 h-3 bg-red-500 rounded-full opacity-50" />
                      <div className="absolute left-[49%] top-[68%] w-3 h-3 bg-red-500 rounded-full opacity-50" />
                      <div className="absolute left-[52%] top-[65%] w-3 h-3 bg-red-500 rounded-full opacity-50" />
                      <div className="absolute left-[22%] top-[29%] w-3 h-3 bg-red-500 rounded-full opacity-50" />
                    </>
                  )}
                </div>

                {/* Map Controls */}
                <div className="absolute top-4 right-4 flex flex-col gap-2">
                  <Button variant="secondary" size="icon" className="h-9 w-9 bg-white dark:bg-gray-700 shadow-md">
                    <Plus className="h-4 w-4" />
                  </Button>
                  <Button variant="secondary" size="icon" className="h-9 w-9 bg-white dark:bg-gray-700 shadow-md">
                    <Minus className="h-4 w-4" />
                  </Button>
                  <Button variant="secondary" size="icon" className="h-9 w-9 bg-white dark:bg-gray-700 shadow-md">
                    <Layers className="h-4 w-4" />
                  </Button>
                  <Button variant="secondary" size="icon" className="h-9 w-9 bg-white dark:bg-gray-700 shadow-md">
                    <Info className="h-4 w-4" />
                  </Button>
                </div>

                {/* Map Layers */}
                <div className="absolute bottom-4 left-4 bg-white dark:bg-gray-800 p-3 rounded-lg border dark:border-gray-700 shadow-md">
                  <h3 className="text-sm font-semibold mb-2 dark:text-white">Map Layers</h3>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Flame className="h-4 w-4 text-orange-500" />
                        <Label htmlFor="show-fires" className="text-sm dark:text-gray-300">
                          Recent Fires
                        </Label>
                      </div>
                      <Switch id="show-fires" checked={showFirePoints} onCheckedChange={setShowFirePoints} />
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Layers className="h-4 w-4 text-blue-500" />
                        <Label htmlFor="show-historical" className="text-sm dark:text-gray-300">
                          Historical Hotspots
                        </Label>
                      </div>
                      <Switch id="show-historical" checked={showHistorical} onCheckedChange={setShowHistorical} />
                    </div>
                  </div>
                </div>
              </div>

              {/* Burn Assessment Summary */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>Controlled Burn Assessment</span>
                    <Badge className={cn(
                      selectedCounty.suitabilityScore >= 80 ? "bg-emerald-500" : 
                      selectedCounty.suitabilityScore >= 60 ? "bg-amber-400" : 
                      "bg-red-600"
                    )}>
                      {selectedCounty.suitabilityScore >= 80 ? "Highly Suitable" : 
                       selectedCounty.suitabilityScore >= 60 ? "Suitable with Caution" : 
                       "Not Recommended"}
                    </Badge>
                  </CardTitle>
                  <CardDescription>
                    Location: {selectedCounty.name} ({selectedCounty.coordinates})
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="text-sm font-semibold mb-2">Suitability Score: {selectedCounty.suitabilityScore}/100</h4>
                    <div className="h-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div 
                        className={cn(
                          "h-full rounded-full", 
                          selectedCounty.suitabilityScore >= 80 ? "bg-emerald-500" : 
                          selectedCounty.suitabilityScore >= 60 ? "bg-amber-400" : 
                          "bg-red-600"
                        )}
                        style={{ width: `${selectedCounty.suitabilityScore}%` }}
                      />
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold mb-2">Potential Limitations</h4>
                    <div className="space-y-2">
                      {burnLimitations.map((limitation, index) => (
                        <div key={index} className="bg-gray-50 dark:bg-gray-800 p-3 rounded-md">
                          <div className="flex items-start">
                            <AlertCircle className="h-5 w-5 text-amber-500 mt-0.5 flex-shrink-0" />
                            <div className="ml-2">
                              <h5 className="text-sm font-medium">{limitation.title}</h5>
                              <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">{limitation.description}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold mb-2">Recommendations</h4>
                    <ul className="space-y-2">
                      {burnRecommendations.map((recommendation, index) => (
                        <li key={index} className="flex items-start">
                          <CheckCircle2 className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                          <span className="ml-2 text-sm">{recommendation}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button variant="outline" onClick={handleExport}>
                    <Download className="h-4 w-4 mr-2" />
                    Export Assessment
                  </Button>
                  <Button 
                    variant={selectedCounty.suitabilityScore >= 60 ? "default" : "secondary"} 
                    onClick={handleSendWarning}
                    disabled={selectedCounty.suitabilityScore < 60}
                  >
                    <Flame className="h-4 w-4 mr-2" />
                    {selectedCounty.suitabilityScore >= 60 ? "Initiate Burn Protocol" : "Not Recommended"}
                  </Button>
                </CardFooter>
              </Card>

              {/* Summary Stats */}
              <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Burn Suitability</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      <span className={getSuitabilityColor(selectedCounty.suitabilityScore)}>{selectedCounty.suitabilityScore}/100</span>
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Based on weather, terrain, and historical data
                    </p>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Hazard Proximity</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold flex items-center">
                      <Badge className={cn("mr-2", getHazardColor(selectedCounty.hazardProximity))}>
                        {selectedCounty.hazardProximity}
                      </Badge>
                      Risk
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Proximity to buildings, power lines, and flammable materials
                    </p>
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm font-medium">Readiness Status</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold flex items-center">
                      <Badge className={cn("mr-2", selectedCounty.permitStatus.toLowerCase() === "approved" ? "bg-emerald-500" : "bg-amber-400")}>
                        {selectedCounty.permitStatus}
                      </Badge>
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {selectedCounty.firePersonnel} personnel ready with {selectedCounty.equipmentStatus.toLowerCase()} equipment
                    </p>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </TooltipProvider>
  )
} 