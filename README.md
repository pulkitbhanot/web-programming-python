# Project 0

Web Programming with Python and JavaScript

Your website must contain at least four different .html pages, and it should be possible to get from any page on your website to any other page by following one or more hyperlinks.

> There are 6 html pages for the project0. Instead of creating a personal webpage I have decided to create a site to display Cricket world cup details. My details are present under the About section.
  I am using the Navbar bootstrap component to display a header information across all the pages. Also the tooltip information is displayed when the mouse hoovers over the first icon in the navbar.
  The navbar is used across all the html pages to enable visiting of any page from any other page.

Your website must include at least one list (ordered or unordered), at least one table, and at least one image.
> there are several lists across different pages
>> index.html
>> author.html
>> author_hobbies.html
>> author_contact.html
  Used 2 images one for the home icon and one for the author images

Your website must have at least one stylesheet file.
> The stylesheet file is project0_stylesheet.css which is generated from project0_stylesheet.scss

Your stylesheet(s) must use at least five different CSS properties, and at least five different types of CSS selectors. You must use the #id selector at least once, and the .class selector at least once.
> Several styling properties are configured using CSS, some of these include font-family, font-size, background-color, font-weight, border, padding, text-align, content.
  CSS selectors are configured for element type selectors, Id selector, Class selector, Child selector, pseudo-element selector. Id selector is used in points_table and fixtures html pages.
  Class selectors are used across several files.

Your stylesheet(s) must include at least one mobile-responsive @media query, such that something about the styling changes for smaller screens.
> @media print is used to remove the navbar for print from fixtures and points_table pages.
  @media screen is also used in the author.html file to hide the author images when the screen resolution becomes <600px

You must use Bootstrap 4 on your website, taking advantage of at least one Bootstrap component, and using at least two Bootstrap columns for layout purposes using Bootstrap’s grid model.

> bootstrap version 4.3.1 is used in the project. Additionally https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js, https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js, https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js are also used in the project to enable the navbar. tooltip component is also used. fixtures and points table has tables which adjust columns with the browser size

Your stylesheets must use at least one SCSS variable, at least one example of SCSS nesting, and at least one use of SCSS inheritance.
> font-color-blue and font-color-red variables are used for SCSS, SCSS nesting is used to display the top headlines section on the main page and the green text on top of the table in fixtures page. SCSS inheritance is used to display author, landing and points_landing text.

In README.md, include a short writeup describing your project, what’s contained in each file, and (optionally) any other additional information the staff should know about your project.
> Some examples were referred on https://www.w3schools.com to understand how to use different html and bootstrap components. The cricket world cup information has been obtained from https://www.espncricinfo.com/
