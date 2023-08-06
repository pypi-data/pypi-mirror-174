import base64
import os

from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from pyallied.web.webWaits import customwebDriverwait


class common_v2(customwebDriverwait):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def findElementsBy(self, locatorType: str, locator):
        try:
            if (super().WaitFor_presence_of_all_elements_located_AnyLocatorType(locatorType, locator)):
                return super().WaitFor_presence_of_all_elements_located_AnyLocatorType(locatorType, locator)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

        # self.driver.presence_of_all_elements_located(xpath)
        # self.driver.visibility_of_element_located(xpath)

    def findElementBy(self, locatorType: str, locator):
        try:
            # self.driver.presence_of_element_located(xpath)
            # self.driver.visibility_of_element_located(xpath)
            if (super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)):
                return super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            else:
                self.__raise_element_not_present_exception(locator)
                raise error
        except Exception as error:
            raise error

    def click(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if (elementPresense):
                if (elementVisible):
                    elementVisible.click()
                else:
                    self.__raise_element_not_visible_exception(locator)
                # raise error
            else:
                self.__raise_element_not_present_exception(locator)
            # raise error
        except Exception as error:
            raise error

    def clear(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if (elementPresense):
                if (elementVisible):
                    elementVisible.clear()
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def isClickable(self, locatorType: str, locator, index=None):
        # self.driver.visibility_of_element_located(xpath)
        try:
            # return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((xpath)))
            return super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
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

    def fillField(self, locatorType: str, locator, text):
        try:
            elementPresence = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisibility = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if (elementPresence):
                if (elementVisibility):
                    elementVisibility.send_keys(text)
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
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

    def getAttribute(self, locatorType: str, locator, AttributeName):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if (elementPresense):
                # if(elementVisible):
                return elementPresense.get_attribute(AttributeName)
            else:
                self.__raise_element_not_present_exception(locator)
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

    def getDomAttribute(self, locatorType: str, locator, AttributeName):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if (elementPresense):
                # if(elementVisible):
                return elementPresense.get_dom_attribute(AttributeName)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    '''
        Gets the given property of the element.

        Args:	
        name - Name of the property to retrieve.
        Usage:	
        text_length = target_element.get_property("text_length")
    '''

    def getProperty(self, locatorType: str, locator, PropertyName):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if (elementPresense):
                # if(elementVisible):
                return elementPresense.get_property(PropertyName)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    '''
        Whether the element is visible to a user.
    '''

    def isElementDisplayed(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if (elementPresense):
                if (elementVisible):
                    return elementVisible.is_displayed()
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    '''
        Returns whether the element is enabled.
    '''

    def isElementEnabled(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if (elementPresense):
                if (elementVisible):
                    return elementVisible.is_enabled()
                else:
                    self.__raise_element_not_visible_exception(locator)
        except Exception as error:
            raise error

    '''
        Returns whether the element is selected.
        Can be used to check if a checkbox or radio button is selected.
    '''

    def isElementSelected(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if (elementPresense):
                if (elementVisible):
                    return elementVisible.is_selected()
                else:
                    self.__raise_element_not_visible_exception(locator)
        except Exception as error:
            raise error

    def isElementDisplayed_v1(self, locatorType: str, locator):
        try:
            if (locatorType.upper() == "XPATH"):
                return self.driver.find_element(By.XPATH, locator).is_displayed()
            elif (locatorType.upper() == "ID"):
                return self.driver.find_element(By.ID, locator).is_displayed()
            elif (locatorType.upper() == "CLASS_NAME"):
                return self.driver.find_element(By.CLASS_NAME, locator).is_displayed()
            elif (locatorType.upper() == "CSS_SELECTOR"):
                return self.driver.find_element(By.CSS_SELECTOR, locator).is_displayed()
            elif (locatorType.upper() == "LINK_TEXT"):
                return self.driver.find_element(By.LINK_TEXT, locator).is_displayed()
            elif (locatorType.upper() == "NAME"):
                return self.driver.find_element(By.NAME, locator).is_displayed()
            elif (locatorType.upper() == "PARTIAL_LINK_TEXT"):
                return self.driver.find_element(By.PARTIAL_LINK_TEXT, locator).is_displayed()
            elif (locatorType.upper() == "TAG_NAME"):
                return self.driver.find_element(By.TAG_NAME, locator).is_displayed()
            else:
                raise Exception(" ** wrong selector/ no selector ** ", locatorType.upper())
        except Exception as error:
            raise error

    '''
        Returns whether the element is enabled.
    '''

    def isElementEnabled_v2(self, locatorType: str, locator):
        try:
            if (locatorType.upper() == "XPATH"):
                return self.driver.find_element(By.XPATH, locator).is_enabled()
            elif (locatorType.upper() == "ID"):
                return self.driver.find_element(By.ID, locator).is_enabled()
            elif (locatorType.upper() == "CLASS_NAME"):
                return self.driver.find_element(By.CLASS_NAME, locator).is_enabled()
            elif (locatorType.upper() == "CSS_SELECTOR"):
                return self.driver.find_element(By.CSS_SELECTOR, locator).is_enabled()
            elif (locatorType.upper() == "LINK_TEXT"):
                return self.driver.find_element(By.LINK_TEXT, locator).is_enabled()
            elif (locatorType.upper() == "NAME"):
                return self.driver.find_element(By.NAME, locator).is_enabled()
            elif (locatorType.upper() == "PARTIAL_LINK_TEXT"):
                return self.driver.find_element(By.PARTIAL_LINK_TEXT, locator).is_enabled()
            elif (locatorType.upper() == "TAG_NAME"):
                return self.driver.find_element(By.TAG_NAME, locator).is_enabled()
            else:
                raise Exception(" ** wrong selector/ no selector ** ", locatorType.upper())
        except Exception as error:
            raise error

    '''
        Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
    '''

    def isElementSelected_v2(self, locatorType: str, locator):
        try:
            if (locatorType.upper() == "XPATH"):
                return self.driver.find_element(By.XPATH, locator).is_selected()
            elif (locatorType.upper() == "ID"):
                return self.driver.find_element(By.ID, locator).is_selected()
            elif (locatorType.upper() == "CLASS_NAME"):
                return self.driver.find_element(By.CLASS_NAME, locator).is_selected()
            elif (locatorType.upper() == "CSS_SELECTOR"):
                return self.driver.find_element(By.CSS_SELECTOR, locator).is_selected()
            elif (locatorType.upper() == "LINK_TEXT"):
                return self.driver.find_element(By.LINK_TEXT, locator).is_selected()
            elif (locatorType.upper() == "NAME"):
                return self.driver.find_element(By.NAME, locator).is_selected()
            elif (locatorType.upper() == "PARTIAL_LINK_TEXT"):
                return self.driver.find_element(By.PARTIAL_LINK_TEXT, locator).is_selected()
            elif (locatorType.upper() == "TAG_NAME"):
                return self.driver.find_element(By.TAG_NAME, locator).is_selected()
            else:
                raise Exception(" ** wrong selector/ no selector ** ", locatorType.upper())
        except Exception as error:
            raise error

    '''
        Saves a screenshot of the current element to a PNG image file. Returns
        False if there is any IOError, else returns True. Use full paths in your filename.
    '''

    def currentElementScreenshot(self, locatorType: str, locator, screenShotSavingPath):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if (elementPresense):
                if (elementVisible):
                    return elementVisible.screenshot(screenShotSavingPath)
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    # action class

    def actionClick(self, locatorType: str, locator):
        try:

            actions = ActionChains(self.driver)
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            # elementLocated=super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                if elementVisible:
                    actions.move_to_element(elementVisible).click(elementVisible)
                    actions.perform()
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

        '''
        Holds down the left mouse button on an element.

        Args:	
        on_element: The element to mouse down. If None, clicks on current mouse position.
        '''

    def actionClickandHold(self, locatorType: str, locator=None):
        try:
            actions = ActionChains(self.driver)
            if (locator != None):
                elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
                elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
                if elementPresense:
                    if elementVisible:
                        actions.click_and_hold(elementVisible)
                        actions.perform()
                    else:
                        self.__raise_element_not_visible_exception(locator)
                else:
                    self.__raise_element_not_present_exception(locator)

            else:
                actions.click_and_hold()
                actions.perform()
        except Exception as error:
            raise error

    '''
    Moves the mouse to the element
    '''

    def moveToElement(self, locatorType: str, locator):
        try:
            actions = ActionChains(self.driver)
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if elementPresense:
                if elementVisible:
                    actions.move_to_element(elementVisible).perform()
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    '''
    Moves the mouse to the element and clicks it
    '''

    def moveToElement_and_click(self, locatorType: str, locator):
        try:
            actions = ActionChains(self.driver)
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if elementPresense:
                if elementVisible:
                    actions.move_to_element(elementVisible).click(elementVisible).perform()
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
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

    def moveToElement_and_subElement_click(self, locatorType: str, LocatorMovingTO, LocatorOfElemtToClick=None):
        try:
            actions = ActionChains(self.driver)
            if (LocatorOfElemtToClick != None):
                elementPresense_LocatorMovingTO = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType,
                                                                                                            LocatorMovingTO)
                elementVisible_LocatorMovingTO = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(
                    locatorType, LocatorMovingTO)
                elementPresense_LocatorOfElemtToClick = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(
                    locatorType, LocatorOfElemtToClick)
                elementVisible_LocatorOfElemtToClick = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(
                    locatorType, LocatorOfElemtToClick)

                if elementPresense_LocatorMovingTO:
                    if elementVisible_LocatorMovingTO:
                        if elementPresense_LocatorOfElemtToClick:
                            if elementVisible_LocatorOfElemtToClick:
                                actions.move_to_element(elementVisible_LocatorMovingTO).click(
                                    elementVisible_LocatorOfElemtToClick).perform()
                            else:
                                self.__raise_element_not_visible_exception(LocatorOfElemtToClick)
                        else:
                            self.__raise_element_not_present_exception(LocatorOfElemtToClick)
                    else:
                        self.__raise_element_not_visible_exception(LocatorMovingTO)
                else:
                    self.__raise_element_not_present_exception(LocatorMovingTO)


            else:
                elementPresense_LocatorMovingTO = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType,
                                                                                                            LocatorMovingTO)
                elementVisible_LocatorMovingTO = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(
                    locatorType, LocatorMovingTO)
                if elementPresense_LocatorMovingTO:
                    if elementVisible_LocatorMovingTO:
                        actions.move_to_element(elementVisible_LocatorMovingTO).click().perform()
                    else:
                        self.__raise_element_not_visible_exception(LocatorMovingTO)
                else:
                    self.__raise_element_not_present_exception(LocatorMovingTO)

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

    def moveToElementWithOffset(self, locatorType: str, locator, xoffset, yoffset):
        try:
            actions = ActionChains(self.driver)
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if elementPresense:
                if elementVisible:
                    actions.move_to_element_with_offset(elementVisible, xoffset, yoffset)
                    actions.perform()
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def moveByOffsett(self, xoffset, yoffset):
        try:
            actions = ActionChains(self.driver)
            actions.move_by_offset(xoffset, yoffset)
            actions.perform()
        except Exception as error:
            raise error

    '''         
    def actionRelease(self, xpath=None):
        try:
            actions = ActionChains(self.driver)
            if(xpath != None):
                if(super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType,locator)):
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

    def keyDown_and_sendKeys(self, ModifierKey: Keys, keys, locatorType=None, locator=None):
        try:
            actions = ActionChains(self.driver)
            if (locator != None and locatorType != None):
                elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
                elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
                if elementPresense:
                    if elementVisible:
                        actions.key_down(ModifierKey, elementVisible).send_keys(keys)
                        actions.perform()
                    else:
                        self.__raise_element_not_visible_exception(locator)
                else:
                    self.__raise_element_not_present_exception(locator)
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

    def keyUp(self, ModifierKey: Keys, locatorType, locator=None):
        try:
            actions = ActionChains(self.driver)
            if (locator != None):
                elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
                elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
                if elementPresense:
                    if elementVisible:
                        actions.key_up(ModifierKey, elementVisible).perform()
                    else:
                        self.__raise_element_not_visible_exception(locator)
                else:
                    self.__raise_element_not_present_exception(locator)

            else:

                actions.key_up(ModifierKey).perform()
        except Exception as error:
            raise error
        '''
         keyboard key press down --> keyboard send keys -->keyboard releasing the key 
        '''

    def keyDown_sendKeys_keyUP(self, ModifierKey: Keys, keys: str, locatorType, locator=None):
        try:
            actions = ActionChains(self.driver)
            if (locator != None):
                elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
                elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
                if elementPresense:
                    if elementVisible:
                        actions.key_down(ModifierKey, elementVisible).send_keys(keys).key_up(ModifierKey,
                                                                                             elementVisible).perform()
                    else:
                        self.__raise_element_not_visible_exception(locator)
                else:
                    self.__raise_element_not_present_exception(locator)
            else:
                actions.key_down(ModifierKey).send_keys(keys).key_up(ModifierKey).perform()
        except Exception as error:
            raise error

    '''
    Double-clicks an element.

    Args:	
    on_element: The element to double-click. If None, clicks on current mouse position.
    '''

    def double_click(self, locatorType: str, locator: None):
        try:
            actions = ActionChains(self.driver)
            if (locator != None):
                elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
                elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
                if elementPresense:
                    if elementVisible:
                        actions.double_click(elementVisible)
                        actions.perform()
                    else:
                        self.__raise_element_not_visible_exception(locator)
                else:
                    self.__raise_element_not_present_exception(locator)

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

    def right_Click(self, locatorType: str, locator=None):
        try:
            actions = ActionChains(self.driver)
            if (locator != None):
                elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
                elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
                if elementPresense:
                    if elementVisible:
                        actions.context_click(elementVisible)
                        actions.perform()
                    else:
                        self.__raise_element_not_visible_exception(locator)
                else:
                    self.__raise_element_not_present_exception(locator)
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

    def sendKeysToElement(self, locatorType: str, locator, *keys_to_send):
        try:
            actions = ActionChains(self.driver)
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if elementPresense:
                if elementVisible:
                    actions.click(elementVisible)
                    actions.send_keys_to_element(elementVisible, *keys_to_send)
                    actions.perform()
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
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
        and the element is not in the viewport, the bottom of the element will first be scrolled to the bottom of the viewport.

        Args:	
        origin: Where scroll originates (viewport or element center) plus provided offsets.
        delta_x: Distance along X axis to scroll using the wheel. A negative value scrolls left.
        delta_y: Distance along Y axis to scroll using the wheel. A negative value scrolls up.
        Raises:	If the origin with offset is outside the viewport. - MoveTargetOutOfBoundsException - If the origin with offset 
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

    def scroll_to_Element(self, locatorType: str, locator):
        try:
            actions = ActionChains(self.driver)
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                # actions.scroll_to_element( elementVisible)
                actions.perform()
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def switch_To_ActiveElement(self):
        try:

            element = self.driver.switch_to.active_element
            return element
        except Exception as error:
            raise error

    def formSubmit(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                elementPresense.submit()
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def get_Value_of_css_property(self, locatorType: str, locator, property_name):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.value_of_css_property(property_name)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def get_Accessible_name(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.accessible_name
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def get_Aria_role(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.Aria_role
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    '''Internal ID used by selenium.

    Internal ID used by selenium.

    This is mainly for internal use. Simple use cases such as checking if 2 webelements refer to the same element, can be done using ==:

    if element1 == element2:
        print("These 2 are equal")
    '''

    def Get_internal_ID(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.id
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def Get_location_of_Element(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.location
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    '''
    THIS PROPERTY MAY CHANGE WITHOUT WARNING. Use this to discover where on the screen an element is 
    so that we can click it. This method should cause the element to be scrolled into view.

    Returns the top lefthand corner location on the screen, or None if the element is not visible.
    '''

    def get_Scroll_location_of_Element(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.location_once_scrolled_into_view
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    '''
    Internal reference to the WebDriver instance this element was found from.
    '''

    def get_Prent_of_Element(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.parent
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    '''
    A dictionary with t he size and location of the element.
    '''

    def get_size_And_Location(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.rect
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def get_element_screenshot_as_base64(self, locatorType: str, locator, name: str):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if elementPresense:
                if elementVisible:
                    with open(self.__webElement_Screenshot_Location() + "/" + name + ".jpg", "wb") as fh:
                        fh.write(base64.urlsafe_b64decode(elementVisible.screenshot_as_base64))
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)

                # return element.screenshot_as_base64
        except Exception as error:
            raise error

    def get_element_screenshot_as_png(self, locatorType: str, locator, name: str):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType, locator)
            if elementPresense:
                if elementVisible:
                    result_File = self.__webElement_Screenshot_Location() + "/" + name + ".png"
                    with open(result_File, "wb") as fh:
                        fh.write(elementVisible.screenshot_as_png)
                else:
                    self.__raise_element_not_visible_exception(locator)
            else:
                self.__raise_element_not_present_exception(locator)
                # Image.open(result_File).save(result_File, 'PNG')
        except Exception as error:
            raise error

    '''
    shadow_root¶
    Returns a shadow root of the element if there is one or an error. Only works from Chromium 96 onwards. Previous versions of Chromium based browsers will throw an assertion exception.

    Returns:	
    ShadowRoot object or
    NoSuchShadowRoot - if no shadow root was attached to element
    
    '''

    def get_Element_shadow_root(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.shadow_root
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def get_Element_size(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.size
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def get_Element_tag_name(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.tag_name
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def get_Element_text(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisible = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,locator)
            if elementPresense:
                # if elementVisible:
                return elementPresense.text
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def __webElement_Screenshot_Location(self):
        try:
            dir_name = os.getcwd() + "/webElement_Screenshots"
            os.makedirs(dir_name, exist_ok=True)
            return dir_name
        except FileExistsError:
            pass

    def __with_findElement_withAnyLocator(self, locatorType: str, locator):

        # if locatorType == "XPATH":
        try:
            element = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)

            return element
        except Exception as error:
            return error

    '''
        drag_and_drop(source, target)¶
        Holds down the left mouse button on the source element,
        then moves to the target element and releases the mouse button.
        Args:	
        source: The element to mouse down.
        target: The element to mouse up
    '''

    def dragAndDrop(self, locatorType: str, sourcexpath, destinationxpath):
        try:
            SourceelElementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType,
                                                                                                sourcexpath)
            SourceelElementVisibility = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,
                                                                                                     sourcexpath)
            DestinationElementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType,
                                                                                                   destinationxpath)
            DestinationElementVisibility = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,
                                                                                                        destinationxpath)
            if (SourceelElementPresense):
                if DestinationElementPresense:
                    if (SourceelElementVisibility):
                        if DestinationElementVisibility:
                            action_chains = ActionChains(self.driver)
                            action_chains.drag_and_drop(SourceelElementVisibility,
                                                        DestinationElementVisibility).perform()
                        else:
                            self.__raise_element_not_visible_exception(destinationxpath)
                    else:
                        self.__raise_element_not_visible_exception(sourcexpath)
                else:
                    self.__raise_element_not_present_exception(sourcexpath)
            else:
                self.__raise_element_not_present_exception(destinationxpath)

        except Exception as error:
            raise error
        '''
        drag_and_drop_by_offset(source, xoffset, yoffset)¶
        Holds down the left mouse button on the source element,
        then moves to the target offset and releases the mouse button.
        Args:	
        source: The element to mouse down.
        xoffset: X offset to move to.
        yoffset: Y offset to move to.
        '''

    def dragAndDropByOffset(self, locatorType: str, sourcexpath, xoffset, yoffset):
        try:
            SourceelElementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType,
                                                                                                sourcexpath)
            SourceelElementVisibility = super().WaitFor_Visibility_of_Element_Located_AnyLocatorType(locatorType,
                                                                                                     sourcexpath)
            if (SourceelElementPresense):
                if (SourceelElementVisibility):
                    action_chains = ActionChains(self.driver)
                    action_chains.drag_and_drop_by_offset(
                        SourceelElementVisibility, xoffset, yoffset).perform()
                else:
                    self.__raise_element_not_visible_exception(sourcexpath)
            else:
                self.__raise_element_not_present_exception(sourcexpath)
        except Exception as error:
            raise error

    def selectDropDownByValue(self, locatorType: str, locator, valueToSelect):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            if (elementPresense):
                # if(elementVisibility):
                select = Select(self.findElementBy(locatorType, locator))
                select.select_by_value(valueToSelect)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def selectDropDownByIndex(self, locatorType: str, locator, indexToSelect):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            if (elementPresense):
                # if(elementVisibility):
                select = Select(self.findElementBy(locatorType, locator))
                select.select_by_index(indexToSelect)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def selectDropDownByVisibleText(self, locatorType: str, locator, textToSelect):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            if (elementPresense):
                select = Select(self.findElementBy(locatorType, locator))
                select.select_by_visible_text(textToSelect)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def deselectAllOptionsInDropDown(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            if (elementPresense):
                # if(elementVisibility):
                select = Select(self.findElementBy(locatorType, locator))
                select.deselect_all()
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def getDefaultSelectedDropDownOptions(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            selectedOptions = []
            if (elementPresense):
                # if(elementVisibility):
                select = Select(self.findElementBy(locatorType, locator))
                all_selected_options = select.all_selected_options
                for i in all_selected_options:
                    if (i.text):
                        selectedOptions.append(i.text)
                    elif (i.get_attribute('value')):
                        selectedOptions.append(i.get_attribute('value'))
                return selectedOptions
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def getAllOptionInDropDown(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            allOptions = []
            if (elementPresense):
                # if(elementVisibility):
                select = Select(self.findElementBy(locatorType, locator))
                options = select.options
                for i in options:
                    if (i.text):
                        allOptions.append(i.text)
                    elif (i.get_attribute('value')):
                        allOptions.append(i.get_attribute('value'))

                return allOptions
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def deselectByIndex(self, locatorType: str, locator, index):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            if (elementPresense):
                # if(elementVisibility):
                select = Select(self.findElementBy(locatorType, locator))
                select.deselect_by_index(index)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def deselectByValue(self, locatorType: str, locator, value):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            if (elementPresense):
                # if(elementVisibility):
                select = Select(self.findElementBy(locatorType, locator))
                select.deselect_by_value(value)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def deselectByVisibleText(self, locatorType: str, locator, text):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            if (elementPresense):
                # if(elementVisibility):
                select = Select(self.findElementBy(locatorType, locator))
                select.deselect_by_visible_text(text)
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def getFirstSelecteOption(self, locatorType: str, locator):
        try:
            elementPresense = super().WaitFor_PresenseOf_Element_Located_AnyLocatorType(locatorType, locator)
            # elementVisibility=super().WaitFor_VisibilityOf_Element_Located(xpath)
            firstSelectedOption = []
            if (elementPresense):
                # if(elementVisibility):
                select = Select(self.findElementBy(locatorType, locator))
                selectedOption = select.first_selected_option
                # for i in selectedOption:
                if (selectedOption.text):
                    firstSelectedOption.append(selectedOption.text)
                elif (selectedOption.get_attribute('value')):
                    firstSelectedOption.append(selectedOption.get_attribute('value'))

                return firstSelectedOption
            else:
                self.__raise_element_not_present_exception(locator)
        except Exception as error:
            raise error

    def switch_To_Frame_ByAnyLocator(self, locatorType: str, locator):
        try:
            # self.driver.presence_of_element_located(frameXpath)
            return super().WaitFor_frame_to_be_available_and_switch_to_it_AnyLocator(locatorType, locator)
            # element=self.findElementBy(locatorType, locator)
            # self.driver.switch_to.frame(element)
        except Exception as error:
            raise error

    def __raise_element_not_present_exception(self, locator):
        raise Exception("element not present : " + locator)

    def __raise_element_not_visible_exception(self, locator):
        raise Exception("element not visible : " + locator)
