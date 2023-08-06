import base64
import os

from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pyallied.web.webWaits import customwebDriverwait


class common(customwebDriverwait):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def findElementsBy(self, xpath):
        try:
            if super().WaitFor_presence_of_all_elements_located(xpath):
                return self.driver.find_elements(By.XPATH, xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

        # self.driver.presence_of_all_elements_located(xpath)
        # self.driver.visibility_of_element_located(xpath)

    def findElementBy(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    return element_visible
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)

        except Exception as error:
            raise error

    def click(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    element_visible.click()
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def clear(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    element_visible.clear()
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def isClickable(self, xpath, index=None):
        # self.driver.visibility_of_element_located(xpath)
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    # return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((xpath)))
                    return element_visible
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    '''
    Simulates typing into the element.

    Args:	
    value - A string for typing, or setting form fields. For setting file inputs, this could be a local file path.
    Use this to send simple key events or to fill out form fields:
    form_textfield = driver.find_element(By.NAME, 'username')
                    form_textfield.send_keys("admin")
    This can also be used to set file inputs.

    file_input = driver.find_element(By.NAME, 'profilePic')
    file_input.send_keys("path/to/profilepic.gif")
    # Generally it's better to wrap the file path in one of the methods
    # in os.path to return the actual path to support cross OS testing.
    # file_input.send_keys(os.path.abspath("path/to/profilepic.gif"))
    '''

    def fillField(self, xpath, text):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visibility = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visibility:
                    element_visibility.send_keys(text)
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def navigateto(self, urlstring):
        try:
            self.driver.get(urlstring)
        except Exception as error:
            raise error

    '''
        Gets the given attribute or property of the element.

        This method will first try to return the value of a property with the given name. If a property with that name doesn’t exist, it returns the value of the attribute with the same name. If there’s no attribute with that name, None is returned.

        Values which are considered truthy, that is equals “true” or “false”, are returned as booleans. All other non-None values are returned as strings. For attributes or properties which do not exist, None is returned.

        To obtain the exact value of the attribute or property, use get_dom_attribute() or get_property() methods respectively.

        Args:	
        name - Name of the attribute/property to retrieve.
        Example:

        # Check if the "active" CSS class is applied to an element.
        is_active = "active" in target_element.get_attribute("class")
    '''

    def getAttribute(self, xpath, AttributeName):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if(element_visible):
                return element_presence.get_attribute(AttributeName)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    '''
        Gets the given attribute of the element. Unlike get_attribute(), this method only returns 
        attributes declared in the element’s HTML markup.

        Args:	
        name - Name of the attribute to retrieve.
        Usage:	
        text_length = target_element.get_dom_attribute("class")
    '''

    def getDomAttribute(self, xpath, AttributeName):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if(element_visible):
                return element_presence.get_dom_attribute(AttributeName)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    '''
        Gets the given property of the element.

        Args:	
        name - Name of the property to retrieve.
        Usage:	
        text_length = target_element.get_property("text_length")
    '''

    def getProperty(self, xpath, PropertyName):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if(element_visible):
                return element_presence.get_property(PropertyName)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def isElementDisplayed(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.is_displayed()
            # else:
            # self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def isElementEnabled(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.is_enabled()
            # else:
            # self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)

        except Exception as error:
            raise error

    def isElementSelected(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    return element_visible.is_selected()
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    '''
        Whether the element is visible to a user.
    '''

    def isElementDisplayed_v2(self, xpath):
        try:
            return self.driver.find_element_by_xpath(xpath).is_displayed()

        except Exception as error:
            raise error

    '''
        Returns whether the element is enabled.
    '''

    def isElementEnabled_v2(self, xpath):
        try:

            return self.driver.find_element_by_xpath(xpath).is_enabled()

        except Exception as error:
            raise error

    '''
        Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
    '''

    def isElementSelected_v2(self, xpath):
        try:

            return self.driver.find_element_by_xpath(xpath).is_selected()

        except Exception as error:
            raise error

    '''
        Saves a screenshot of the current element to a PNG image file. Returns
        False if there is any IOError, else returns True. Use full paths in your filename.
    '''

    def currentElementScreenshot(self, xpath, screenShotSavingPath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    return element_visible.screenshot(screenShotSavingPath)
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    # action class

    def actionClick(self, xpath):
        try:
            actions = ActionChains(self.driver)
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                # element = self.driver.find_element(By.XPATH, xpath)
                actions.move_to_element(element_presence).click(element_presence)
                actions.perform()
                # else:
                # self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def action_clear_field(self, xpath):
        try:
            actions = ActionChains(self.driver)
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                # element = self.driver.find_element(By.XPATH, xpath)
                actions.click(element_presence).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(
                    Keys.BACK_SPACE).pause(1).perform()
            # else:
            # self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

        '''
        Holds down the left mouse button on an element.

        Args:	
        on_element: The element to mouse down. If None, clicks on current mouse position.
        '''

    def actionClickandHold(self, xpath=None):
        try:
            actions = ActionChains(self.driver)
            if (xpath != None):
                element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
                # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
                if element_presence:
                    # if element_visible:
                    actions.click_and_hold(element_presence)
                    actions.perform()
                # else:
                # self.__raise_element_not_visible_exception(xpath)
                else:
                    self.__raise_element_not_present_exception(xpath)
            else:
                actions.click_and_hold()
                actions.perform()
        except Exception as error:
            raise error

    '''
    Moves the mouse to the element
    '''

    def moveToElement(self, xpath):
        try:
            actions = ActionChains(self.driver)
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                # element = self.driver.find_element(By.XPATH, xpath)
                actions.move_to_element(element_presence).perform()
            # else:
            # self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    '''
    Moves the mouse to the element and clicks it
    '''

    def moveToElement_and_click(self, xpath):
        try:
            actions = ActionChains(self.driver)
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                # element = self.driver.find_element(By.XPATH, xpath)
                actions.move_to_element(element_presence).click(element_presence).perform()
            # else:
            # self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error
        '''
        if both xpathOfMovingTO and xpathOfElemtToClick are provided, it will click the subemenet like below example
        ex:
        actions = ActionChains(driver)
        actions.move_to_element(menu)
        actions.click(hidden_submenu)
        actions.perform()
        if user didnt provide subelement xpath, then it clicks the same element mouse moved to
        '''

    def moveToElement_and_subElement_click(self, xpathOfMovingTO, xpathOfElemtToClick=None):
        try:
            actions = ActionChains(self.driver)
            if (xpathOfElemtToClick != None):

                element_presence_OfMovingTo = super().WaitFor_PresenseOf_Element_Located(xpathOfMovingTO)
                # element_visible_OfMovingTo = super().WaitFor_VisibilityOf_Element_Located(xpathOfMovingTO)
                element_presence_ToClick = super().WaitFor_PresenseOf_Element_Located(xpathOfElemtToClick)
                # element_visible_ToClick = super().WaitFor_VisibilityOf_Element_Located(xpathOfElemtToClick)
                if element_presence_OfMovingTo:
                    # if element_visible_OfMovingTo:
                    if element_presence_ToClick:
                        # if element_visible_ToClick:
                        # MovedToelement = self.driver.find_element(By.XPATH, xpathOfMovingTO)
                        # ClickElement=  self.driver.find_element(By.XPATH, xpathOfElemtToClick)
                        actions.move_to_element(element_presence_OfMovingTo).click(
                            element_presence_OfMovingTo).perform()
                    # else:
                    # self.__raise_element_not_visible_exception(xpathOfElemtToClick)
                    else:
                        self.__raise_element_not_present_exception(xpathOfElemtToClick)
                # else:
                # self.__raise_element_not_visible_exception(xpathOfMovingTO)
                else:
                    self.__raise_element_not_present_exception(xpathOfMovingTO)

            else:
                element_presence_OfMovingTo = super().WaitFor_PresenseOf_Element_Located(xpathOfMovingTO)
                # element_visible_OfMovingTo = super().WaitFor_VisibilityOf_Element_Located(xpathOfMovingTO)
                if element_presence_OfMovingTo:
                    # if element_visible_OfMovingTo:
                    # MovedToelement = self.driver.find_element(By.XPATH, xpathOfMovingTO)

                    actions.move_to_element(element_presence_OfMovingTo).click().perform()
                # else:
                # self.__raise_element_not_visible_exception(xpathOfMovingTO)
                else:
                    self.__raise_element_not_present_exception(xpathOfMovingTO)
        except Exception as error:
            raise error
        '''
            Move the mouse by an offset of the specified element.
            Offsets are relative to the top-left corner of the element.
            Args:	
            to_element: The WebElement to move to.
            xoffset: X offset to move to.
            yoffset: Y offset to move to.
        '''

    def moveToElementWithOffset(self, xpath, xoffset, yoffset):
        try:
            actions = ActionChains(self.driver)
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                # element = self.driver.find_element(By.XPATH, xpath)
                actions.move_to_element_with_offset(element_presence, xoffset, yoffset)
                actions.perform()
            # else:
            # self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def moveToElement_WithOffset_and_click(self, xpath, xoffset, yoffset):
        try:
            actions = ActionChains(self.driver)
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                # element = self.driver.find_element(By.XPATH, xpath)
                actions.move_to_element_with_offset(element_presence, xoffset, yoffset).click()
                actions.perform()
            # else:
            # self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def moveTo_location_and_click(self, xoffset, yoffset, clickElementXpath=None):
        try:
            actions = ActionChains(self.driver)

            if clickElementXpath != None:
                element_presence = super().WaitFor_PresenseOf_Element_Located(clickElementXpath)
                # element_visible = super().WaitFor_VisibilityOf_Element_Located(clickElementXpath)
                if element_presence:
                    # if element_visible:
                    # element = self.driver.find_element(By.XPATH, clickElementXpath)
                    actions.move_to_location(xoffset, yoffset).click(element_presence)
                    actions.perform()
                # else:
                # self.__raise_element_not_visible_exception(clickElementXpath)
                else:
                    self.__raise_element_not_present_exception(clickElementXpath)
            else:
                actions.move_to_location(xoffset, yoffset).click()
                actions.perform()
        except Exception as error:
            raise error

    '''
    move_by_offset(xoffset, yoffset)¶
    Moving the mouse to an offset from current mouse position.

    Args:	
    xoffset: X offset to move to, as a positive or negative integer.
    yoffset: Y offset to move to, as a positive or negative integer.

    '''

    def moveByOffsett(self, xoffset, yoffset):
        try:
            actions = ActionChains(self.driver)
            actions.move_by_offset(xoffset, yoffset)
            actions.perform()
        except Exception as error:
            raise error

    def move_ByOffset_and_click(self, xoffset, yoffset):
        try:
            actions = ActionChains(self.driver)
            actions.move_by_offset(xoffset, yoffset).click()
            actions.perform()
        except Exception as error:
            raise error

    '''         
    def actionRelease(self, xpath=None):
        try:
            actions = ActionChains(self.driver)
            if(xpath != None):
                if(super().WaitFor_PresenseOf_Element_Located(xpath)):
                    element = self.driver.find_element(By.XPATH, xpath)
            else:
                element = None
            if(element != None):
                actions.release(element)
                actions.perform()

            else:
                actions.release()
                actions.perform()
        except Exception as error:
            raise error        
    '''

    def keyDown_and_sendKeys(self, ModifierKey: Keys, keys, xpath=None):
        try:
            actions = ActionChains(self.driver)
            if (xpath != None):
                element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
                element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
                if element_presence:
                    if element_visible:
                        # element = self.driver.find_element(By.XPATH, xpath)
                        actions.key_down(ModifierKey, element_visible).send_keys(keys)
                        actions.perform()
                    else:
                        self.__raise_element_not_visible_exception(xpath)
                else:
                    self.__raise_element_not_present_exception(xpath)
            else:
                actions.key_down(ModifierKey).send_keys(keys)
                actions.perform()
        except Exception as error:
            raise error

    '''
    Releases a modifier key.

    Args:	
    value: The modifier key to send. Values are defined in Keys class.
    element: The element to send keys. If None, sends a key to current focused element.
    Example, pressing ctrl+c:

    ActionChains(driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    
    '''

    def keyUp(self, ModifierKey: Keys, xpath=None):
        try:
            actions = ActionChains(self.driver)
            if (xpath != None):
                element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
                element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
                if element_presence:
                    if element_visible:
                        # element = self.driver.find_element(By.XPATH, xpath)
                        actions.key_up(ModifierKey, element_visible).perform()
                    else:
                        self.__raise_element_not_visible_exception(xpath)
                else:
                    self.__raise_element_not_present_exception(xpath)
            else:

                actions.key_up(ModifierKey).perform()
        except Exception as error:
            raise error
        '''
         keyboard key press down --> keyboard send keys -->keyboard releasing the key 
        '''

    def keyDown_sendKeys_keyUP(self, ModifierKey: Keys, keys: str, xpath=None):
        try:
            actions = ActionChains(self.driver)
            if (xpath != None):
                element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
                element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
                if element_presence:
                    if element_visible:
                        # element = self.driver.find_element(By.XPATH, xpath)
                        actions.key_down(ModifierKey, element_visible).send_keys(keys).key_up(ModifierKey,
                                                                                              element_visible).perform()
                    else:
                        self.__raise_element_not_visible_exception(xpath)
                else:
                    self.__raise_element_not_present_exception(xpath)
            else:
                actions.key_down(ModifierKey).send_keys(keys).key_up(ModifierKey).perform()
        except Exception as error:
            raise error

    '''
    Double-clicks an element.

    Args:	
    on_element: The element to double-click. If None, clicks on current mouse position.
    '''

    def double_click(self, xpath: None):
        try:
            actions = ActionChains(self.driver)
            if (xpath != None):
                element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
                element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
                if element_presence:
                    if element_visible:
                        # element = self.driver.find_element(By.XPATH, xpath)
                        actions.double_click(element_visible)
                        actions.perform()
                    else:
                        self.__raise_element_not_visible_exception(xpath)
                else:
                    self.__raise_element_not_present_exception(xpath)
            else:
                actions.double_click()
                actions.perform()
        except Exception as error:
            raise error

        '''
        Performs a context-click (right click) on an element.

        Args:	
        on_element: The element to context-click. If None, clicks on current mouse position.
        '''

    def right_Click(self, xpath=None):
        try:
            actions = ActionChains(self.driver)
            if (xpath != None):
                element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
                element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
                if element_presence:
                    if element_visible:
                        actions.context_click(element_visible)
                        actions.perform()
                    else:
                        self.__raise_element_not_visible_exception(xpath)
                else:
                    self.__raise_element_not_present_exception(xpath)
            else:
                actions.context_click()
                actions.perform()
        except Exception as error:
            raise error

    def resetActions(self):
        try:
            actions = ActionChains(self.driver)
            actions.reset_actions()
            actions.perform()
        except Exception as error:
            raise error

    def sendKeys(self, *keys_to_send):
        try:
            actions = ActionChains(self.driver)
            actions.send_keys(*keys_to_send)
            actions.perform()
        except Exception as error:
            raise error

    def sendKeysToElement(self, xpath, *keys_to_send):
        try:
            actions = ActionChains(self.driver)
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    # element = super().WaitFor_PresenseOf_Element_Located(xpath)
                    actions.click(element_visible)
                    actions.send_keys_to_element(element_visible, *keys_to_send)
                    actions.perform()
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

        '''
        Sends wheel scroll information to the driver to be processed.

        Args:	
        x: starting X coordinate
        y: starting Y coordinate
        delta_x: the distance the mouse will scroll on the x axis
        delta_y: the distance the mouse will scroll on the y axis

        '''

    def Scroll(self, x: int, y: int, delta_x: int, delta_y: int, duration: int = 0, origin: str = 'viewport'):
        try:
            actions = ActionChains(self.driver)

            actions.scroll(x, y, delta_x, delta_y, duration, origin)
            actions.perform()
        except Exception as error:
            raise error

        '''
        Scrolls by provided amounts with the origin in the top left corner of the viewport.

    Args:	
    delta_x: Distance along X axis to scroll using the wheel. A negative value scrolls left.
    delta_y: Distance along Y axis to scroll using the wheel. A negative value scrolls up.
        '''

    def Scroll_by_amount(self, delta_x: int, delta_y: int):
        try:
            actions = ActionChains(self.driver)

            actions.scroll_by_amount(delta_x, delta_y)
            actions.perform()
        except Exception as error:
            raise error
        '''
        Scrolls by provided amount based on a provided origin. The scroll origin is either the center of an 
        element or the upper left of the viewport plus any offsets. If the origin is an element, 
        and the element is not in the viewport, the bottom of the element will first be scrolled to the bottom of the 
        viewport.

        Args:	
        origin: Where scroll originates (viewport or element center) plus provided offsets.
        delta_x: Distance along X axis to scroll using the wheel. A negative value scrolls left.
        delta_y: Distance along Y axis to scroll using the wheel. A negative value scrolls up.
        Raises:	If the origin with offset is outside the viewport. - MoveTargetOutOfBoundsException - If the origin 
        with offset 
        is outside the viewport.
        '''

    def Scroll_from_origin(self, scroll_origin: ScrollOrigin, delta_x: int, delta_y: int):
        try:
            actions = ActionChains(self.driver)

            actions.scroll_from_origin(scroll_origin, delta_x, delta_y)
            actions.perform()
        except Exception as error:
            raise error

        '''
                If the element is outside the viewport, scrolls the bottom of the element to the bottom of the viewport.

        Args:	
        element: Which element to scroll into the viewport.
        send_keys(*keys_to_send)
        Sends keys to current focused element.

        Args:	
        keys_to_send: The keys to send. Modifier keys constants can be found in the ‘Keys’ class.
        '''

    def scroll_to_Element(self, xpath):
        try:
            actions = ActionChains(self.driver)
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                # element = self.driver.find_element(By.XPATH, xpath)
                actions.scroll_to_element(element_presence)
                actions.perform()
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def switch_To_ActiveElement(self):
        try:

            self.driver.switch_to.active_element
        except Exception as error:
            raise error

    def formSubmit(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    element_visible.submit()
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def get_Value_of_css_property(self, xpath, property_name):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.value_of_css_property(property_name)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def get_Accessible_name(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.accessible_name
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def get_Aria_role(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.Aria_role
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    '''Internal ID used by selenium.

    Internal ID used by selenium.

    This is mainly for internal use. Simple use cases such as checking if 2 webelements refer to the same element, can be done using ==:

    if element1 == element2:
        print("These 2 are equal")
    '''

    def Get_internal_ID(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.id
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def Get_location_of_Element(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.location
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    '''
    THIS PROPERTY MAY CHANGE WITHOUT WARNING. Use this to discover where on the screen an element is 
    so that we can click it. This method should cause the element to be scrolled into view.

    Returns the top lefthand corner location on the screen, or None if the element is not visible.
    '''

    def get_Scroll_location_of_Element(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.location_once_scrolled_into_view
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def scroll_into_view_by_js(self, xpath):
        element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
        if element_presence:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", self.driver.find_element_by_xpath(xpath))
        else:
            self.__raise_element_not_present_exception(xpath)

    def clear_input_field_by_js(self, xpath):
        element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
        if element_presence:
            self.driver.execute_script("arguments[0].value = '';", self.driver.find_element_by_xpath(xpath))
        else:
            self.__raise_element_not_present_exception(xpath)

    '''
    Internal reference to the WebDriver instance this element was found from.
    '''

    def get_Prent_of_Element(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.parent
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    '''
    A dictionary with t he size and location of the element.
    '''

    def get_size_And_Location(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.rect
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def get_element_screenshot_as_base64(self, xpath, name: str):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    with open(self.__webElement_Screenshot_Location() + "/" + name + ".jpg", "wb") as fh:
                        fh.write(base64.urlsafe_b64decode(element_visible.screenshot_as_base64))
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
                # return element.screenshot_as_base64
        except Exception as error:
            raise error

    def get_element_screenshot_as_png(self, xpath, name: str):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                if element_visible:
                    result_File = self.__webElement_Screenshot_Location() + "/" + name + ".png"
                    with open(result_File, "wb") as fh:
                        fh.write(element_visible.screenshot_as_png)
                        # Image.open(result_File).save(result_File, 'PNG')
                else:
                    self.__raise_element_not_visible_exception(xpath)
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    '''
    shadow_root¶
    Returns a shadow root of the element if there is one or an error. Only works from Chromium 96 onwards. Previous versions of Chromium based browsers will throw an assertion exception.

    Returns:	
    ShadowRoot object or
    NoSuchShadowRoot - if no shadow root was attached to element
    
    '''

    def get_Element_shadow_root(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.shadow_root
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def get_Element_size(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.size
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def get_Element_tag_name(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.tag_name
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def click_by_js(self, xpath):
        try:
            if super().WaitFor_PresenseOf_Element_Located(xpath):
                self.driver.execute_script("arguments[0].click;", self.driver.find_element_by_xpath(xpath))
        except Exception as error:
            raise error

    def get_Element_text(self, xpath):
        try:
            element_presence = super().WaitFor_PresenseOf_Element_Located(xpath)
            # element_visible = super().WaitFor_VisibilityOf_Element_Located(xpath)
            if element_presence:
                # if element_visible:
                return element_presence.text
            else:
                self.__raise_element_not_present_exception(xpath)
        except Exception as error:
            raise error

    def __webElement_Screenshot_Location(self):
        try:
            dir_name = os.getcwd() + "/webElement_Screenshots"
            os.makedirs(dir_name, exist_ok=True)
            return dir_name
        except FileExistsError:
            pass

    def __with_findElement_withAnyLocator(self, locatorType, locator):

        # if locatorType == "XPATH":
        try:
            element = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)

            return element
        except Exception as error:
            return error

    def __raise_element_not_present_exception(self, locator):
        raise Exception("element not present : " + locator)

    def __raise_element_not_visible_exception(self, locator):
        raise Exception("element not visible : " + locator)
