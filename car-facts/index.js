'use strict';
var Alexa = require('alexa-sdk');

var APP_ID = undefined; //OPTIONAL: replace with "amzn1.echo-sdk-ams.app.[your-unique-value-here]";
var SKILL_NAME = 'Car Facts';

/**
 * Array containing space facts.
 */
var FACTS = [
    "About 165,000 cars are produced every day.",
    "The new car smell is composed of over 50 volatile organic compounds.",
    "It would take less than 6 months to get to the Moon by car at 60mph or 95km/h.",
    "Hitler, while in prison, wrote to a Mercedes dealership begging for a car loan.",
    "Up to 19 girls can be crammed into a smart car.",
    "The average car has 30,000 parts.",
    "92% of all new sold cars in Brazil use ethanol as fuel, which is produced from sugar cane.",
    "75% of cars that Rolls-Royce has ever produced are still on the road today.",
    "Volkswagen owns Bentley, Bugatti, Lamborghini, Audi, Ducati and Porsche.",
    "The average American spends about 38 hours a year stuck in traffic.",
    "The first car accident occurred in 1891, in Ohio.",
    "The odds of dying in a car accident are around 1 in 5,000.",
    "When the car radio was introduced, some states wanted to ban it arguing that it could distract drivers and cause accidents.",
    "It is a criminal offence to drive around in a dirty car in Russia.",
    "Car wrecks are the number one cause of death for Americans under 35.",
    "In Turkmenistan, car drivers are entitled to 120 Liters (31 gal.) of free petrol a month.",
    "There are more cars than people in Los Angeles.",
    "The inventor of the cruise control was blind.",
    "The vehicle with the highest mileage covered a total of 2,850,000 miles or 4,586,630 km.",
    "The world's fastest street-legal production car is the Bugatti Veyron Super Sport, at 267 mph or 431 km/h.",
    "In 1941, Henry Ford made a car out of soybeans.",
    "Most new cars fake engine noise through speakers. They are quite silent otherwise.",
    "Honking your car horn, except in an emergency, is illegal in NYC.",
    "Sweden's Volvo made the three-point seatbelt design patent open and available to other car manufacturers for free, in the interest of safety. It saves one life every 6 minutes.",
    "95% of a car's lifetime is spent parked.",
    "During a car crash, 40% of drivers never even hit the brakes.",
    "In the early years of the 20th century, horses were causing so much pollution with their poop that cars were seen as the green alternative.",
    "It costs US$8,876 per year to own and maintain an average car in the U.S. That's US$443,800 in 50 years.",
    "In 2012, Nevada became the first state to issue licenses for self-driving cars.",
    "It is possible to set up a holiday meal inside a car's engine compartment and drive long enough to fully cook all of the food.",
    "Up to 80% of an average car is recyclable.",
    "In 1900, 40% of American cars were powered by steam, 38% by electricity, and 22% by gasoline.",
    "5% of the world's population drives on the left side of the road.",
    "Parking takes up as much as 14% of all land-use in Los Angeles County.",
    "Hummer drivers get almost 5 times as many tickets as the U.S. national average for all vehicles, according to a 2009 study.",
    "The average Bugatti customer has about 84 cars, 3 jets and one yacht.",
    "Joe Ranft, co-writer and co-director on the film Cars, died in a car accident while the movie was still in production.",
    "The inventor of intermittent windshield wipers tried to sell his idea to the auto industry and was turned away. When they began showing up on new cars, he sued, and won.",
    "Traffic accidents kill 1.25 million people per year.",
    "Having no recollection of your drive to work or school (autopilot) is called Highway Hypnosis.",
    "The top speed at the world's first real automobile race in 1895 was just 15 mph.",
    "Texting while driving increases the chances of a crash by 23 times.",
    "Americans wasted US$2 billion in 2015 putting premium gasoline into cars that don't need it.",
    "Road traffic accidents kill more people around the world than malaria.",
    "Each year up to 50 million people are injured in traffic accidents, globally.",
    "A recent study estimates that mass-adoption of self-driving cars could reduce over 90% of traffic accidents.",
    "American commuters collectively waste 5.5 billion hours per year in traffic, releasing into the atmosphere an unnecessary 56 billion pounds of CO2.",
    "The standard service of a Bugatti Veyron would cost you US$21,000.",
    "Companies like Tesla, Uber and Google are working to make self-driving cars a reality"
];

exports.handler = function(event, context, callback) {
    var alexa = Alexa.handler(event, context);
    alexa.APP_ID = APP_ID;
    alexa.registerHandlers(handlers);
    alexa.execute();
};

var handlers = {
    'LaunchRequest': function () {
        this.emit('GetFact');
    },
    'GetNewFactIntent': function () {
        this.emit('GetFact');
    },
    'GetFact': function () {
        // Get a random space fact from the space facts list
        var factIndex = Math.floor(Math.random() * FACTS.length);
        var randomFact = FACTS[factIndex];

        // Create speech output
        var speechOutput = "Here's your fact: " + randomFact;

        this.emit(':tellWithCard', speechOutput, SKILL_NAME, randomFact)
    },
    'AMAZON.HelpIntent': function () {
        var speechOutput = "You can say tell me a car fact, or, you can say exit... What can I help you with?";
        var reprompt = "What can I help you with?";
        this.emit(':ask', speechOutput, reprompt);
    },
    'AMAZON.CancelIntent': function () {
        this.emit(':tell', 'Goodbye!');
    },
    'AMAZON.StopIntent': function () {
        this.emit(':tell', 'Goodbye!');
    }
};