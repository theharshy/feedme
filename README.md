# FeedMe: A Cloud-Based Restaurant Management System

## Contents

- [Abstract](#abstract)
- [Introduction](#-introduction)
- [Architecture](#architecture)
- [License](#license)

## Abstract

As restaurants increasingly move towards prioritizing delivery across delivery services, there is a growing need to effectively facilitate customer engagement. Restaurant SEO is heavily based upon review count and overall reviews. Unfortunately, each delivery service has its own app for customer engagement and none of them heavily focus on guiding restaurant goers to leave reviews. This would require using 5 logins for 1 restaurant to handle customer engagement for a single branch, 10 logins for 2 branches and so on. There are three goals of FeedMe: 1) centralize user engagement through the development of aggregated feeds across all delivery platforms and for all branches of a single restaurant, 2) spur increased review numbers through sending restaurant goers automated messages with tailored links associated with the review sites alongside a nice message, and 3) create a web-based chatting service that can communicate with restaurant goers through text messages (we also hope to allow for group chats to allow for mass marketing messaging for delivery coupons or new menu updates). We’ve created the initial version of the application using our cloud architecture and are excited to share it with you.

## Introduction

With the food delivery market expected to grow to $365 billion globally by 2030, restaurateurs—be they franchises or individuals—have been eagerly searching for ways to capitalize on the delivery boom, both because it is operationally prudent, but also because customers are demanding it. Third-party delivery platforms, like Uber Eats and DoorDash, have accelerated this growth, so much so that an entirely novel type of restaurant has been increasingly popping up in major cities—delivery-only/virtual restaurants and cloud kitchens. For restaurants, SEO optimization on Google and within these apps are crucial as this determines their positioning on listings for users and users are much more likely to choose restaurants with more reviews and higher on listings.
The goal is to design an interaction management system for these restaurants to allow them to effectively gauge feedback/reviews from consumers and unique drive brand development. This approach has been extremely successful for small to medium businesses (SMBs) and the same can be replicated for delivery restaurants. Once a restaurant gets an email or text indicating that an order has been placed and has been fulfilled, this data will be scraped to generate a text message or email that will be sent to thank the user and offer them a link to a page that will allow them to:

* Leave unique feedback (or menu recommendations) for the restaurant through text messaging the restaurant* Sass ready with lots of commenting
* Leave reviews on Google Reviews, Yelp, or Open Table
* (in the future) Talk to a chatbot about their restaurant experience (how the customer’s experience can be improved? Any difficulties faced during the process? etc).

This page will have an easy to use interface to guide individuals through each of these workflows.
From the restaurant’s perspective, they will have three interfaces that can help them understand their customer engagement:
1. A user dashboard that shows the number of overall reviews, stars, and growth metrics for engagement.
2. An engagement flow that shows the responses left by each user. When a specific user is clicked, the restaurant can see the message left, any conversational information, and can also text/email the user back to discuss the experience overall.
3. A feedback page showing the unique feedback and menu recommendations left to the user.
Restaurants can also offer rewards to users who leave reviews through this mechanism. This tool is incredibly useful for restaurants that deliver through multiple locations and multiple delivery services as it decreases the amount of research work needed to drive this feedback and respond to it. This application would be a one-stop shop for all customer engagement for restaurants.


## Architecture

From an architecture perspective, the entire web application is built using a very AWS-heavy stack. As the main intention of this application required high scalability and low latency (to fulfill real-time engagement and messaging), it is highly dependent on serverless products like Lambda, provided by AWS. As mentioned earlier, from the restaurant’s perspective, there are three key perspectives: the analytics dashboard, the engagement feeds, and the messaging functionality. These 3 interfaces are hosted as static pages on S3 behind Cognito for User Authentication/Security. We use a Swagger-based API gateway to interface with our microservice-focused serverless architecture (as can be seen in the diagram below). Our
Lambdas extensively use DynamoDB or ElasticSearch to facilitate our key functionalities. We used ElasticSearch mainly for chat storage, search optimization, analytics numbers and other functions that were very search heavy. We used Dynamo for more traditional storage. Aside from these views, we had key functionalities driven by lambda for analytics, chatting, and order onboarding. We used SES to receive inbound emails to registered email accounts for our theoretical restaurants. On an email receipt, the data is written to SQS from which a Lambda will be triggered to scrap the data, extract the key information, and write it to the pertinent databases. Additionally, a text message with a unique order-based link including links for leaving reviews will be sent out. We also used CloudWatch to configure weekly-run lambdas that scrape review analytics on our restaurants from Google, OpenTable, and Yelp and write them to our analytics tables (this lambda is also used to run aggregations on our own data for further analytics on order types, popular delivery services, etc). All of our texting services are driven through Twilio. For outbound messages, we use the simple SDK. For inbound messages, we have a Lambda-based webhook that appropriately scrapes the message metadata, assigns it to the proper reviewer and restaurant, and proceeds to handle the data properly (write to ElasticSearch, SQS, etc). We use SQS extensively to populate new user notifications based on new engagements/inbound messages to allow for easy user understanding.

### Making Edits / Customizing the Template

To setup, simply fork the repo and run `npm install` in order to get all the Gulp dev dependencies. Next, run `Gulp watch` to compile the Sass and minify the JavaScript. Alternatively, if you don't have Gulp installed globally, you can run the npm script `npm run watch`. Any changes done to the JavaScript (js/scripts.js) or Sass (sass/styles.scss) will be autocompiled and ready to go.

All scripts are within `js/scripts.js` and get minified to `js/scripts.min.js`. All styles are in `sass/styles.scss` and get compiled to `css/styles.css`. Both the minified scripts file and compiled CSS file are what is loaded on the page by default.

At this point, the page is ready to go and you can begin to add your own information and make any needed changes. The sections below  contains a quick breakdown of each of the default sections and how they work.

### Using The Template As Is

If you wish to use the template as is (i.e. how it's seen in the demo), then all that's required is the `css`, `images`, `js`, `libs` folders and the `index.html` file. You would then add your content to `index.html` as needed and you're good to go!

## Customization and Editing

### General

In general, most styles on the page are based off the definitions of variables in the variable section of the style sheet:

```SCSS
// Define base and accent colors
$base-color: #3498db;
$base-color-hover: darken($base-color, 10%);

// Define background colors
$background: #fff;
$background-alt: #f2f2f5;

// Define border colors
$border: #dcd9d9;

// Define text colors
$heading: #374054;
$text: #74808a;
```

If you wish to change the general colour scheme of the page for example, simply change the value of `$base-color`.

There is also a number of default CSS classes that can be applied such as `.shadow`, `.shadow-large`, `.btn-rounded-white`, and various others. These can be found under the General Styles section in the style sheet.

### Images

By default, the template comes with a number of images, some of which can be kept and others which act simply as placeholders and should be switched. The template contains the following:

* Main background (images/lead-bg.jpg) - this is the main background image provided via [Unsplash](https://unsplash.com/). This can be kept or changed easily by replacing `images/lead-bg.jpg` with your new background (recommended size of at least 1920x1080).
* Favicon (/favicon.ico) - this is the favicon used for the page. Similar to the main bg, this can kept or changed easily by replacing the `favicon.ico` with your new one.
* Project image - these are the images associated with the projects under the project section. These are simply placeholders and should either be replaced or removed.

### Header Section

The header section can be found within the `<header>` tag and simply contains an unordered list of anchors to different sections of the page. If you add a new section and want to be able to quickly navigate to it from the top, simply add another list element with an anchor that has the href of the ID of the section. Conversely, if you remove a section, don't forget to remove the associated navigation element.

If you wish to add a header link to an external page, simply add the class `no-scroll` to the anchor. For example:

```HTML
<li>
    <a href="https://google.com" class="no-scroll">Google</a>
</li>
```

If you wish to have a sticky (fixed) header, you simply need to add a class of `sticky` to the main header. For example, that would be accomplished as follows:

```HTML
<header class="sticky">
    <!-- Header content -->
</header>
```

### Lead Section

The Lead section is pretty straightforward, it contains an h1 for your name and an h2 for your title. It also contains a link that can be used to link to your resume should you wish to add it as well.

If you want your resume to automatically download when the button is clicked instead of opening up in another tab (the default behaviour), add the following code (Thanks to jkfran for the suggestion) in the lead:

```HTML
<a href="path/to/resume.pdf" download="resume.pdf" class="btn-rounded-white">Download Resume</a>
```

The href attribute points to where your resume is stored and the download attribute is what triggers the download / provides the name the file will be downloaded as when the user clicks the button (In this case, it will download as resume.pdf).

### About Section

The about section contains a quick about blurb that can be edited by changing the text within the paragraph tags.

### Experience Section

The experience section creates a vertical timeline with all your relevant experience. The code for the timeline creation can be found within `js/scripts.js` and is an adaptaion of [RyanFitzgerald/vertical-timeline](https://github.com/RyanFitzgerald/vertical-timeline).

The default format is as follows:

```HTML
<div id="experience-timeline">
    <div data-date="September 2015 – September 2016">
        <h3>Employer Name</h3>
        <h4>Job Title</h4>
        <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur in iaculis ex.
        </p>
    </div>
</div>
```

The data attribute `data-date` is what is used to add a date to the associated timeline point. All that is really required is a wrapping div (i.e. `#experience-timeline`) and nested divs to build the timeline. The h3, h4, and p tags are optional and the contents of the div can be styled however you wish.

To add additional section, simply add additional nested divs under the main wrapping div.

### Education Section

The Education is just a series of `.education-block` classes with some details associated with them. By default, it shows school name, date, degree, and some additional details. For example:

```HTML
<div class="education-block">
    <h3>University of Ottawa</h3>
    <span class="education-date">Sept 2016 - Sept 2017</span>
    <h4>Bachelor of Science in Computer Science</h4>
    <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur in iaculis ex.
    </p>
</div>
```

To add additional section, simply add additional `.education-block` elements.

### Projects Section

The Project section contains a number of `.project` elements that represent each of your projects. By default, it contains a 300x300 image under `.project-image` and relevant project information under `.project-info`. An example is as follows:

```HTML
<div class="project">
    <div class="project-image">
        <img src="images/project.jpg" />
    </div>
    <!-- End .project-image -->

    <div class="project-info">
        <h3>Project Name Here</h3>
        <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur in iaculis ex.
        </p>
        <a href="#">View Project</a>
    </div>
    <!-- End .project-info -->
</div>
```

If you want to hide some projects by default, you can throw them in an additional row and add the markup for the "Show More" button. This would be done as follows:

```HTML
<!-- Projects Above -->

<a id="view-more-projects" href="#">View More Projects</a>
<div id="more-projects" class="row">
    <div class="project shadow-large">
        <div class="project-image">
            <img src="images/project.jpg" />
        </div>
        <!-- End .project-image -->
        <div class="project-info">
            <h3>Project Name Here</h3>
            <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur in iaculis ex. Etiam volutpat laoreet urna. Morbi ut tortor nec nulla commodo malesuada sit amet vel lacus. Fusce eget efficitur libero. Morbi dapibus porta quam laoreet placerat.
            </p>
            <a href="#">View Project</a>
        </div>
        <!-- End .project-info -->
    </div>
    <!-- End .project -->
</div>
```

This will add a link that says "View More Projects" under the current projects and when clicked, all projects in the "More-projects" div will be shown. This is optional functionality and isn't provided by default. It is important that you keep the wrapping div ID intact ("#more-projects") as well as the anchor ID ("#view-more-projects"), however the contents of the div and the anchor text itself can be edited however you like.

#### Projects without images

If you do not wish to have a project image associated with a project, you can simply add `no-image` as an additional class to the project. It would look like the following:

```HTML
<div class="project no-image">
    <div class="project-info">
        <h3>Project Name Here</h3>
        <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur in iaculis ex.
        </p>
        <a href="#">View Project</a>
    </div>
    <!-- End .project-info -->
</div>
```

### Skills Section

The Skills section is simply an unordered list that spits out a "Skill Cloud" with all the skills listed. To add / remove skills, simply edit or add list elements, like so:

```HTML
<ul>
    <li>JavaScript</li>
    <li>Python</li>
    <li>Ruby</li>
    <li>Go</li>
    <li>Node.js</li>
</ul>
```

### Contact Section

Since the page is static, I opted to use the awesome Formspree to allow for a contact form without the need for anything else. To use it, you must have the page hosted on a server (loading a basic HTML page won't work) where a referrer header is generated. Also, simply add the email to the action. An example is as follows:

```HTML
<form method="POST" action="https://formspree.io/email@email.com">
    <input type="hidden" name="_subject" value="Contact request from personal website" />
    <input type="email" name="_replyto" placeholder="Your email" required>
    <textarea name="message" placeholder="Your message" required></textarea>
    <button type="submit">Send</button>
</form>
```
For more information on configuration of the contact form or dealing with errors, check out [Formspree](https://formspree.io/).

For a quick tutorial about formspree, check out this [tutsplus tutorial](https://webdesign.tutsplus.com/tutorials/quick-tip-add-a-formspree-form-to-your-static-sites--cms-23870) that covers different aspects and features of the form tool.

### Footer Section

The Footer contains an optional copyright where you can place your name as well as an unordered list of all of your social or coding related profiles. By default it contains Github, Stack Overflow, Facebook, Twitter, and Google Plus. You can add or remove them easily and simply use the Font Awesome icon associated with the social profile you wish to use. For a list of all icons, [click here](http://fontawesome.io/icons/).

### Optional Sections

The template comes with an optional section that can be added to the page markup to list things like Certifications, Hobbies, and more (Note: these are not included by default). The markup for the additional optional section is as follows:

```HTML
<div class="optional-section background-alt">
    <h2 class="heading">Section Name</h2>

    <div class="optional-section-block">
        <h3>Some content title</h3>
        <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur in iaculis ex. Etiam volutpat laoreet urna. Morbi ut tortor nec nulla commodo malesuada sit amet vel lacus. Fusce eget efficitur libero. Morbi dapibus porta quam laoreet placerat.
        </p>
        <ul>
            <li>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </li>
            <li>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </li>
            <li>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            </li>
        </ul>
    </div>
    <!-- End .optional-section-block -->

</div>
<!-- End .optional-section -->
```

You can copy .optional-section-block for each new item you wish you have in the optional section. Also, the background-alt class may need to be removed depending on where the optional section is placed in your layout as this adds the grey background. If you play it at the bottom after "Skills", it can be used as is. Also, by default the border is applied at the top, but this can also be adjusted as needed.

The optional section blocks have styling for h3 (the block title), h4, p, and ul tags by default.

## Changelog

### 1.2.2

* Updated dependencies and gulpfile

### 1.2.1

* Updated dependencies and gulpfile
* Added `no-image` optional class for projects without images (see above for usage)

### 1.2.0

* Added support for optional "Show More Projects" that hides some projects by default if included
* Added optional sections to display certifications, languages, etc.

### 1.1.3

* Added default favicon to be used or changed
* Added `sticky` class to make header fixed
* Updated docs to add image section

### 1.1.2

* Added `no-scroll` class option to header navigation anchor if you want to link to external site
* Changed contact form input / textarea colours to be based off `$base-color`
* Changed main background to 100vh so it doesn't overflow if viewport height < 700px

### 1.1.1

* Made input placeholder text more readable
* Removed timeline line when no JS
* Added some basic styling to timeline when no JS

### 1.1.0

* Fixed menu toggle on mobile devices
* Fixed z-index / scrolling issue with mobile menu
* Mobile menu now closes once a nav element is hit

## License

Completely free (MIT)! See [LICENSE.md](LICENSE.md) for more.
