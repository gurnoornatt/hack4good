import Link from "next/link"
import { ArrowRight, CheckCircle, Flame, Globe, BarChart3, Shield, Zap, MapPin } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ThemeToggle } from "@/components/ui/theme-toggle"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-950 flex flex-col">
      {/* Header */}
      <header className="border-b border-gray-200 dark:border-gray-800">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center">
              <Flame className="h-8 w-8 text-red-600" />
              <span className="ml-2 text-xl font-bold text-gray-900 dark:text-white">BurnAI</span>
            </div>
            <div className="flex items-center gap-6">
              <nav className="hidden md:flex space-x-8">
                <a href="#features" className="text-sm font-medium text-gray-700 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                  Features
                </a>
                <a href="#technology" className="text-sm font-medium text-gray-700 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                  Technology
                </a>
                <a href="#testimonials" className="text-sm font-medium text-gray-700 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                  Testimonials
                </a>
                <a href="#pricing" className="text-sm font-medium text-gray-700 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                  Pricing
                </a>
              </nav>
              <div className="flex items-center gap-3">
                <ThemeToggle />
                <Link href="/dashboard" passHref>
                  <Button>
                    Dashboard
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-red-50 to-orange-100 dark:from-gray-900 dark:to-gray-800 z-0"></div>
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-900 dark:text-white leading-tight">
                Advanced Wildfire <span className="text-red-600">Risk Analysis</span> for California
              </h1>
              <p className="mt-6 text-xl text-gray-600 dark:text-gray-300 max-w-2xl">
                BurnAI combines satellite data, weather patterns, and historical fire records to provide real-time wildfire risk assessment and prevention recommendations.
              </p>
              <div className="mt-10 flex flex-col sm:flex-row gap-4">
                <Link href="/dashboard" passHref>
                  <Button size="lg" className="text-base">
                    View Live Dashboard
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Button variant="outline" size="lg" className="text-base">
                  Request Demo
                </Button>
              </div>
              <div className="mt-8 flex items-center">
                <div className="flex -space-x-2">
                  {[1, 2, 3, 4].map((i) => (
                    <div key={i} className={`w-10 h-10 rounded-full border-2 border-white dark:border-gray-800 bg-gray-${i * 100} flex items-center justify-center text-white text-xs font-bold`}>
                      {i === 4 ? '+' : ''}
                    </div>
                  ))}
                </div>
                <p className="ml-4 text-sm text-gray-600 dark:text-gray-400">
                  Trusted by <span className="font-semibold">200+</span> fire departments and agencies across California
                </p>
              </div>
            </div>
            <div className="relative">
              <div className="w-full h-[500px] bg-white dark:bg-gray-800 rounded-xl shadow-xl overflow-hidden">
                <div className="absolute inset-0 bg-[url('/placeholder.svg?height=800&width=1200')] bg-cover bg-center opacity-80"></div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                <div className="absolute bottom-0 left-0 right-0 p-6">
                  <div className="bg-white dark:bg-gray-900 rounded-lg p-4 shadow-lg">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-lg font-semibold">Los Angeles County</h3>
                      <span className="px-2 py-1 bg-amber-400 text-white text-xs font-medium rounded-full">Moderate Risk</span>
                    </div>
                    <div className="h-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full bg-amber-400 rounded-full" style={{ width: "47%" }}></div>
                    </div>
                    <div className="mt-3 grid grid-cols-3 gap-2 text-xs">
                      <div className="text-center">
                        <div className="font-semibold">47/100</div>
                        <div className="text-gray-500 dark:text-gray-400">Risk Score</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold">20</div>
                        <div className="text-gray-500 dark:text-gray-400">Recent Fires</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold">600 MW</div>
                        <div className="text-gray-500 dark:text-gray-400">Heat Output</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="absolute -top-6 -right-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
                <div className="flex items-center gap-2">
                  <Zap className="h-5 w-5 text-amber-500" />
                  <span className="text-sm font-medium">Live Updates</span>
                </div>
              </div>
              <div className="absolute -bottom-6 -left-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
                <div className="flex items-center gap-2">
                  <MapPin className="h-5 w-5 text-red-500" />
                  <span className="text-sm font-medium">Precision Mapping</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white dark:bg-gray-950">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Comprehensive Wildfire Intelligence</h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
              Our platform provides end-to-end wildfire risk management with advanced analytics and actionable insights.
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <Globe className="h-8 w-8 text-blue-500" />,
                title: "Satellite Monitoring",
                description: "Real-time satellite data from MODIS and VIIRS sensors to detect hotspots and active fires across California.",
              },
              {
                icon: <BarChart3 className="h-8 w-8 text-green-500" />,
                title: "Predictive Analytics",
                description: "Machine learning models that predict fire risk based on weather, vegetation, and historical patterns.",
              },
              {
                icon: <Shield className="h-8 w-8 text-red-500" />,
                title: "Risk Assessment",
                description: "County-level risk scores updated daily with detailed breakdowns of contributing factors.",
              },
              {
                icon: <Flame className="h-8 w-8 text-orange-500" />,
                title: "Controlled Burn Planning",
                description: "AI-powered recommendations for preventative controlled burns to reduce wildfire fuel.",
              },
              {
                icon: <Zap className="h-8 w-8 text-yellow-500" />,
                title: "Real-time Alerts",
                description: "Instant notifications for emerging fire threats and changing risk conditions.",
              },
              {
                icon: <MapPin className="h-8 w-8 text-purple-500" />,
                title: "High-Resolution Mapping",
                description: "Detailed maps showing risk zones, active fires, and historical hotspots with precise geolocation.",
              },
            ].map((feature, index) => (
              <div key={index} className="bg-gray-50 dark:bg-gray-900 rounded-xl p-8 shadow-sm hover:shadow-md transition-shadow">
                <div className="bg-white dark:bg-gray-800 rounded-full w-16 h-16 flex items-center justify-center shadow-sm mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{feature.title}</h3>
                <p className="mt-2 text-gray-600 dark:text-gray-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section id="technology" className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Powered by Advanced Technology</h2>
              <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
                Our platform leverages cutting-edge technology to provide the most accurate and timely wildfire risk assessments.
              </p>

              <div className="mt-8 space-y-6">
                {[
                  {
                    title: "NASA FIRMS Integration",
                    description: "Direct integration with NASA's Fire Information for Resource Management System for real-time fire detection.",
                  },
                  {
                    title: "Machine Learning Models",
                    description: "Custom-trained neural networks that analyze multiple data sources to predict fire risk with high accuracy.",
                  },
                  {
                    title: "High-Performance Computing",
                    description: "Cloud-based infrastructure that processes terabytes of satellite and weather data in real-time.",
                  },
                  {
                    title: "Historical Data Analysis",
                    description: "25+ years of historical fire data incorporated into our predictive models for better pattern recognition.",
                  },
                ].map((item, index) => (
                  <div key={index} className="flex">
                    <div className="flex-shrink-0">
                      <CheckCircle className="h-6 w-6 text-green-500" />
                    </div>
                    <div className="ml-4">
                      <h3 className="text-lg font-medium text-gray-900 dark:text-white">{item.title}</h3>
                      <p className="mt-1 text-gray-600 dark:text-gray-400">{item.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-4">
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 transform translate-y-8">
                    <h4 className="font-semibold text-gray-900 dark:text-white">Data Processing</h4>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">15TB+ of satellite imagery processed daily</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                    <h4 className="font-semibold text-gray-900 dark:text-white">Prediction Accuracy</h4>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">92% accuracy in 7-day fire risk forecasts</p>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                    <h4 className="font-semibold text-gray-900 dark:text-white">Update Frequency</h4>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">Risk assessments updated every 3 hours</p>
                  </div>
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 transform translate-y-8">
                    <h4 className="font-semibold text-gray-900 dark:text-white">Coverage Area</h4>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">100% of California's 58 counties monitored</p>
                  </div>
                </div>
              </div>
              <div className="absolute -z-10 inset-0 bg-gradient-to-br from-red-100 to-orange-200 dark:from-red-900/20 dark:to-orange-900/20 rounded-xl transform -rotate-3"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 bg-white dark:bg-gray-950">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Trusted by Fire Management Professionals</h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
              Hear from the fire departments and agencies that rely on BurnAI for critical wildfire management.
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                quote: "BurnAI has transformed how we approach wildfire prevention. The predictive analytics have helped us allocate resources more effectively and prevent several potential disasters.",
                author: "Sarah Johnson",
                title: "Fire Chief, Los Angeles County Fire Department",
                image: "https://randomuser.me/api/portraits/women/32.jpg",
              },
              {
                quote: "The controlled burn recommendations from BurnAI have been invaluable. We've reduced our high-risk areas by 37% in just one fire season by following their guidance.",
                author: "Michael Chen",
                title: "Director, California Department of Forestry and Fire Protection",
                image: "https://randomuser.me/api/portraits/men/46.jpg",
              },
              {
                quote: "As a county with limited resources, BurnAI's risk assessment tools help us focus our prevention efforts where they're needed most. It's like having an extra team of analysts on staff.",
                author: "David Rodriguez",
                title: "Emergency Management Coordinator, San Bernardino County",
                image: "https://randomuser.me/api/portraits/men/22.jpg",
              },
            ].map((testimonial, index) => (
              <div key={index} className="bg-gray-50 dark:bg-gray-900 rounded-xl p-8 shadow-sm">
                <div className="flex items-center mb-6">
                  <div className="flex-shrink-0">
                    <img src={testimonial.image} alt={testimonial.author} className="h-12 w-12 rounded-full" />
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white">{testimonial.author}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{testimonial.title}</p>
                  </div>
                </div>
                <p className="text-gray-600 dark:text-gray-400 italic">"{testimonial.quote}"</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Flexible Plans for Every Need</h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
              Choose the plan that works best for your organization's size and requirements.
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                name: "Basic",
                price: "$499",
                description: "Essential fire risk monitoring for small departments",
                features: [
                  "Daily risk assessments",
                  "County-level monitoring",
                  "Basic alert system",
                  "7-day historical data",
                  "Standard support",
                ],
                cta: "Get Started",
                highlighted: false,
              },
              {
                name: "Professional",
                price: "$999",
                description: "Advanced analytics for medium-sized departments",
                features: [
                  "Hourly risk assessments",
                  "Sub-county precision mapping",
                  "Advanced alert system",
                  "30-day historical data",
                  "Controlled burn recommendations",
                  "Priority support",
                ],
                cta: "Get Started",
                highlighted: true,
              },
              {
                name: "Enterprise",
                price: "Custom",
                description: "Comprehensive solution for large agencies",
                features: [
                  "Real-time risk assessments",
                  "Custom integration options",
                  "Advanced predictive modeling",
                  "Unlimited historical data",
                  "Custom reporting",
                  "24/7 dedicated support",
                ],
                cta: "Contact Sales",
                highlighted: false,
              },
            ].map((plan, index) => (
              <div
                key={index}
                className={`rounded-xl p-8 ${
                  plan.highlighted
                    ? "bg-white dark:bg-gray-800 shadow-xl ring-2 ring-red-500 dark:ring-red-400 relative"
                    : "bg-gray-100 dark:bg-gray-800 shadow-sm"
                }`}
              >
                {plan.highlighted && (
                  <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-red-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                    MOST POPULAR
                  </div>
                )}
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">{plan.name}</h3>
                <div className="mt-4 flex items-baseline">
                  <span className="text-4xl font-extrabold text-gray-900 dark:text-white">{plan.price}</span>
                  <span className="ml-1 text-xl font-medium text-gray-500 dark:text-gray-400">/month</span>
                </div>
                <p className="mt-2 text-gray-600 dark:text-gray-400">{plan.description}</p>

                <ul className="mt-6 space-y-4">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-start">
                      <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                      <span className="ml-3 text-gray-600 dark:text-gray-400">{feature}</span>
                    </li>
                  ))}
                </ul>

                <div className="mt-8">
                  <Button
                    className={`w-full ${
                      plan.highlighted ? "bg-red-600 hover:bg-red-700" : ""
                    }`}
                    variant={plan.highlighted ? "default" : "outline"}
                  >
                    {plan.cta}
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-red-600 to-orange-600 dark:from-red-900 dark:to-orange-900">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white">Ready to Transform Your Wildfire Management?</h2>
          <p className="mt-4 text-xl text-red-100 max-w-2xl mx-auto">
            Join the growing network of fire departments and agencies using BurnAI to protect communities across California.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/dashboard" passHref>
              <Button size="lg" variant="secondary" className="text-base">
                View Live Dashboard
              </Button>
            </Link>
            <Button size="lg" className="text-base bg-white text-red-600 hover:bg-gray-100">
              Schedule a Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center">
                <Flame className="h-8 w-8 text-red-500" />
                <span className="ml-2 text-xl font-bold text-white">BurnAI</span>
              </div>
              <p className="mt-4 text-sm">
                Advanced wildfire risk monitoring and prevention for California's fire management professionals.
              </p>
              <div className="mt-6 flex space-x-4">
                {["twitter", "facebook", "linkedin", "github"].map((social) => (
                  <a key={social} href="#" className="text-gray-400 hover:text-white">
                    <span className="sr-only">{social}</span>
                    <div className="h-6 w-6 rounded-full bg-gray-700 flex items-center justify-center">
                      <span className="text-xs">{social[0].toUpperCase()}</span>
                    </div>
                  </a>
                ))}
              </div>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white uppercase tracking-wider">Product</h3>
              <ul className="mt-4 space-y-2">
                {["Features", "Technology", "Pricing", "Case Studies", "Documentation"].map((item) => (
                  <li key={item}>
                    <a href="#" className="text-gray-400 hover:text-white text-sm">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white uppercase tracking-wider">Company</h3>
              <ul className="mt-4 space-y-2">
                {["About", "Team", "Careers", "Blog", "Press"].map((item) => (
                  <li key={item}>
                    <a href="#" className="text-gray-400 hover:text-white text-sm">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white uppercase tracking-wider">Legal</h3>
              <ul className="mt-4 space-y-2">
                {["Privacy", "Terms", "Security", "Data Processing", "Cookies"].map((item) => (
                  <li key={item}>
                    <a href="#" className="text-gray-400 hover:text-white text-sm">
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="mt-12 border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-gray-400">© 2025 BurnAI, Inc. All rights reserved.</p>
            <div className="mt-4 md:mt-0">
              <ThemeToggle />
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
} 