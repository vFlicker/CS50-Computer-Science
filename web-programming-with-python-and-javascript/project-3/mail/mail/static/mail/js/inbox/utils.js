export const capitalizeFirstLetter = (inputString) => {
    const firstLetter = inputString[0].toUpperCase();
    const restOfTheString = inputString.slice(1);

    return firstLetter + restOfTheString;
}