import React from 'react';
import { Check, Zap, Star, Crown, Sparkles } from 'lucide-react';

const PricingPage = () => {
  const plans = [
    {
      name: 'Free',
      price: '$0',
      period: 'forever',
      description: 'Perfect for getting started with AI file intelligence',
      features: [
        '100 searches per month',
        'Basic file analysis',
        'File categorization',
        'Search history',
        'Community support'
      ],
      limitations: [
        'Limited monthly searches',
        'Basic insights only',
        'No file upload analysis'
      ],
      buttonText: 'Get Started Free',
      buttonColor: 'bg-gray-600 hover:bg-gray-700',
      icon: Sparkles,
      popular: false
    },
    {
      name: 'Pro',
      price: '$9.99',
      period: 'per month',
      description: 'Unlock the full power of Jaymi AI file intelligence',
      features: [
        'Unlimited searches',
        'Advanced file analysis',
        'AI-powered organization',
        'File upload analysis',
        'Smart insights & suggestions',
        'Organization automation',
        'Priority support',
        'Search export'
      ],
      limitations: [],
      buttonText: 'Start Pro Trial',
      buttonColor: 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700',
      icon: Zap,
      popular: true
    },
    {
      name: 'Team',
      price: '$29.99',
      period: 'per month',
      description: 'Advanced features for teams and organizations',
      features: [
        'Everything in Pro',
        'Multi-user dashboard',
        'Team file sharing',
        'Admin analytics',
        'Custom integrations',
        'Advanced security',
        'Dedicated support',
        'Custom training'
      ],
      limitations: [],
      buttonText: 'Contact Sales',
      buttonColor: 'bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700',
      icon: Crown,
      popular: false
    }
  ];

  const features = [
    {
      title: 'Natural Language Search',
      description: 'Search your files using everyday language like "find my photos from last week"',
      icon: '🗣️'
    },
    {
      title: 'AI-Powered Organization',
      description: 'Let AI learn your patterns and automatically organize your files',
      icon: '🧠'
    },
    {
      title: 'Smart Insights',
      description: 'Get actionable insights about your file organization and usage patterns',
      icon: '💡'
    },
    {
      title: 'File Analysis',
      description: 'Comprehensive analysis of your file system with categorization and statistics',
      icon: '📊'
    }
  ];

  return (
    <div className="space-y-16">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">
          Choose Your <span className="gradient-text">Jaymi AI</span> Plan
        </h1>
        <p className="text-xl text-gray-200 mb-8">
          Transform your file management with AI-powered intelligence
        </p>
        <div className="bg-green-500 bg-opacity-20 text-green-300 px-4 py-2 rounded-full inline-block">
          🎉 Special Launch Pricing - Save 50% for the first 3 months!
        </div>
      </div>

      {/* Pricing Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {plans.map((plan, index) => (
          <div
            key={index}
            className={`glass-effect rounded-2xl p-8 relative ${
              plan.popular ? 'ring-2 ring-blue-400 scale-105' : ''
            }`}
          >
            {plan.popular && (
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-full text-sm font-medium flex items-center">
                  <Star className="w-4 h-4 mr-1" />
                  Most Popular
                </div>
              </div>
            )}

            <div className="text-center mb-8">
              <div className={`w-12 h-12 mx-auto mb-4 rounded-xl flex items-center justify-center ${
                plan.name === 'Free' ? 'bg-gray-600' :
                plan.name === 'Pro' ? 'bg-gradient-to-r from-blue-500 to-purple-600' :
                'bg-gradient-to-r from-purple-500 to-pink-600'
              }`}>
                <plan.icon className="w-6 h-6 text-white" />
              </div>
              
              <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
              <p className="text-gray-300 text-sm mb-4">{plan.description}</p>
              
              <div className="mb-4">
                <span className="text-4xl font-bold text-white">{plan.price}</span>
                <span className="text-gray-300 ml-1">/{plan.period}</span>
              </div>

              <button className={`w-full py-3 px-4 rounded-lg font-medium text-white transition-colors ${plan.buttonColor}`}>
                {plan.buttonText}
              </button>
            </div>

            <div className="space-y-4">
              <h4 className="text-white font-semibold">Features included:</h4>
              <ul className="space-y-3">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-center text-gray-300">
                    <Check className="w-4 h-4 text-green-400 mr-3 flex-shrink-0" />
                    <span className="text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              {plan.limitations.length > 0 && (
                <>
                  <h4 className="text-gray-400 font-semibold mt-6">Limitations:</h4>
                  <ul className="space-y-2">
                    {plan.limitations.map((limitation, limitIndex) => (
                      <li key={limitIndex} className="flex items-center text-gray-400">
                        <span className="w-4 h-4 text-red-400 mr-3 text-xs">✕</span>
                        <span className="text-sm">{limitation}</span>
                      </li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Features Showcase */}
      <div className="glass-effect p-12 rounded-2xl">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-white mb-4">
            Why Choose Jaymi AI?
          </h2>
          <p className="text-xl text-gray-200">
            Revolutionary file intelligence that adapts to your workflow
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="flex items-start space-x-4">
              <div className="text-3xl">{feature.icon}</div>
              <div>
                <h3 className="text-white font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-300">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* FAQ Section */}
      <div className="glass-effect p-12 rounded-2xl">
        <h2 className="text-3xl font-bold text-white text-center mb-8">
          Frequently Asked Questions
        </h2>

        <div className="space-y-6">
          <div>
            <h3 className="text-white font-semibold mb-2">Is my data secure?</h3>
            <p className="text-gray-300">
              Absolutely! We process your files locally when possible and use enterprise-grade encryption for any cloud processing. Your data is never shared with third parties.
            </p>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-2">Can I cancel anytime?</h3>
            <p className="text-gray-300">
              Yes! You can cancel your subscription at any time. Your account will remain active until the end of your billing period.
            </p>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-2">What file types are supported?</h3>
            <p className="text-gray-300">
              Jaymi AI supports all common file types including documents, images, videos, audio files, code, and archives. We're constantly adding support for more file types.
            </p>
          </div>

          <div>
            <h3 className="text-white font-semibold mb-2">How does the AI learning work?</h3>
            <p className="text-gray-300">
              Jaymi AI learns from your file organization patterns, search behavior, and preferences to provide increasingly personalized and accurate suggestions over time.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center glass-effect p-12 rounded-2xl">
        <h2 className="text-3xl font-bold text-white mb-4">
          Ready to Transform Your File Management?
        </h2>
        <p className="text-xl text-gray-200 mb-8">
          Join thousands of users who've discovered the power of AI-driven file intelligence
        </p>
        <button className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-lg text-lg font-medium hover:from-blue-600 hover:to-purple-700 transition-colors">
          Start Your Free Trial Today
        </button>
        <p className="text-gray-400 text-sm mt-4">
          No credit card required • 14-day free trial • Cancel anytime
        </p>
      </div>
    </div>
  );
};

export default PricingPage;